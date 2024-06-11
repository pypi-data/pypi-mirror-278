import asyncio
import hashlib
from dataclasses import dataclass, field
from typing import Callable, Any
from itertools import count
import datetime
import time
from abc import ABC, abstractmethod
from DLMS_SPODES.types.implementations import enums, long_unsigneds, bitstrings, octet_string, structs
from DLMS_SPODES import exceptions as exc
from DLMS_SPODES.cosem_interface_classes import collection, overview, ln_pattern
from DLMS_SPODES.types import cdt, ut, cst
from DLMS_SPODES.hdlc import frame
from DLMS_SPODES.enums import Transmit, Application
from DLMS_SPODES.firmwares import get_firmware
from DLMS_SPODES.cosem_interface_classes.image_transfer import image_transfer_status as i_t_status
from .client import Client, pdu, logL, AppVersion, OSI, Status, Security, Data, Conformance, mechanism_id, AcseServiceUser, State


class ExTask(ABC):
    """Exchange task for DLMS client"""
    async def run(self, c: Client):
        """exception handling block"""
        try:
            return await self.physical(c)
        except (ConnectionRefusedError, TimeoutError) as e:
            c.set_error(Transmit.NO_PORT, e.args[0])
            return False  # todo: maybe never connected
        except exc.DLMSException as e:
            c.set_error(e.error, e.args[0])
        except Exception as e:
            c.log(logL.INFO, F'UNKNOWN ERROR: {e}...')
            c.set_error(Transmit.UNKNOWN, F'При обмене{e}')
        except asyncio.CancelledError as e:
            c.set_error(Transmit.ABORT, "ручная остановка")
            await c.close()  # todo: change to DiscRequest
        finally:
            c.received_frames.clear()  # for next exchange need clear all received frames. todo: this bag, remove in future

    async def physical(self, c: Client):
        if OSI.PHYSICAL not in c.level:
            if not c.media.is_open():
                await c.media.open()
            c.level = OSI.PHYSICAL
            c.set_error(Transmit.OK, "Open port")
            c.log(logL.INFO, F"Open port communication channel: {c.media}")
            if c.objects is None:
                await InitType().data_link(c)
                await c.close()  # todo: change to DiscRequest, or make not closed
            ret = await self.data_link(c)
            await c.close()  # todo: change to DiscRequest
            return ret

    async def data_link(self, c: Client, is_public: bool = False):
        if OSI.DATA_LINK not in c.level:
            c.status = Status.EXCHANGE
            c.set_error(Transmit.OK, "Open port")
            c.errors.clear()  # clear all last session errors
            c.send_frames.clear()
            # calculate addresses
            c.DA = frame.Address(
                upper_address=int(c.server_SAP),
                lower_address=int(c.device_address) if c.device_address else None,
                length=c.addr_size
            )
            c.SA = frame.Address(upper_address=0x10 if is_public else int(c.SAP))
            c.log(logL.INFO, F"{c.SA=} {c.DA=}")
            # initialize connection
            c.reply.clear()
            # replace this
            if c.settings.cipher.security != Security.NONE:
                c.log(logL.DEB, F"Security: {c.settings.cipher.security}/n"
                                F"System title: {c.settings.cipher.systemTitle.hex()}"
                                F"Authentication key: {c.settings.cipher.authenticationKey.hex()}"
                                F"Block cipher key: {c.settings.cipher.blockCipherKey.hex()}")
                if c.settings.cipher.dedicatedKey:
                    c.log(logL.DEB, F"Dedicated key: {c.settings.cipher.dedicatedKey.hex()}")
            # SNRM
            c.get_SNRM_request()
            c.status = Status.READ
            await c.read_data_block()
            c.status = Status.EXCHANGE
            c.level = OSI.DATA_LINK
            c.reply.clear()
        return await self.application(c, is_public)

    async def application(self, c: Client, is_public: bool = False):
        if OSI.APPLICATION not in c.level:
            if c.invocationCounter and c.settings.cipher is not None and c.settings.cipher.security != Security.NONE:
                # create IC object. TODO: remove it after close connection, maybe???
                c.settings.proposedConformance |= Conformance.GENERAL_PROTECTION

                # my block
                IC: Data = c.objects.add_if_missing(ut.CosemClassId(1),
                                                    logical_name=cst.LogicalName(bytearray((0, c.get_channel_index(), 43, 1,
                                                                                            c.current_association.security_setup_reference.e, 255))),
                                                    version=cdt.Unsigned(0))
                tmp_client_SAP = c.current_association.associated_partners_id.client_SAP
                challenge = c.settings.ctoSChallenge
                try:
                    c.objects.getIECHDLCSetup(c.get_channel_index()).set_from_info(c.reply.data.get_data())
                    c.aarqRequest(c.m_id)
                    await c.read_data_block()
                    ret = c.parseAareResponse(c.reply.data)
                    c.level |= OSI.APPLICATION  # todo: it's must be result of <ret> look down
                    c.reply.clear()
                    await c.read_attribute(IC, 2)
                    c.settings.cipher.invocationCounter = 1 + IC.value.decode()
                    c.log(logL.DEB, "Invocation counter: " + str(c.settings.cipher.invocationCounter))
                    # disconnect
                    if c.media and c.media.is_open():
                        c.log(logL.DEB, "DisconnectRequest")
                        await c.disconnect_request()
                finally:
                    c.SAP = tmp_client_SAP
                    c.settings.useCustomChallenge = challenge is not None
                    c.settings.ctoSChallenge = challenge

                # gurux with several removed methods
                # add = self.settings.clientAddress
                # auth = self.settings.authentication
                # security = self.client.ciphering.security
                # challenge = self.client.ctoSChallenge
                # try:
                #     self.client.clientAddress = 16
                #     self.settings.authentication = Authentication.NONE
                #     self.client.ciphering.security = Security.NONE
                #     reply = GXReplyData()
                #     self.get_SNRM_request()
                #     self.status = Status.READ
                #     self.read_data_block2()
                #     self.objects.IEC_HDLS_setup.set_from_info(self.reply.data.get_data())
                #     self.connection_state = ConnectionState.HDLC
                #     self.reply.clear()
                #     self.aarqRequest()
                #     self.read_data_block2()
                #     self.parseAareResponse(reply.data)
                #     reply.clear()
                #     item = GXDLMSData(self.invocationCounter)
                #     data = self.client.read(item, 2)[0]
                #     reply = GXReplyData()
                #     self.read_data_block(data, reply)
                #     item.encodings[2] = reply.data.get_data()
                #     Update data type on read.
                #     if item.getDataType(2) == cdt.NullData.TAG:
                #         item.setDataType(2, reply.valueType)
                #     self.client.updateValue(item, 2, reply.value)
                #     self.client.ciphering.invocationCounter = 1 + item.value
                #     print("Invocation counter: " + str(self.client.ciphering.invocationCounter))
                #     if self.media and self.media.isOpen():
                #         self.log(logL.INFO, "DisconnectRequest")
                #         self.disconnect_request()
                # finally:
                #     self.settings.clientAddress = add
                #     self.settings.authentication = auth
                #     self.client.ciphering.security = security
                #     self.client.ctoSChallenge = challenge

            c.aarqRequest(mechanism_id.NONE if is_public else c.m_id)
            await c.read_data_block()
            # await c.read_attr(ut.CosemAttributeDescriptor((collection.ClassID.ASSOCIATION_LN, ut.CosemObjectInstanceId("0.0.40.0.0.255"), ut.CosemObjectAttributeId(6)))) # for test only
            match c.parseAareResponse(c.reply.data):
                case AcseServiceUser.NULL:
                    c.log(logL.INFO, 'Authentication success')
                    c.level |= OSI.APPLICATION
                case AcseServiceUser.AUTHENTICATION_FAILURE as diag if is_public:
                    c.log(logL.WARN, F'On Public connection type got {diag.name}, broad force turn ON')
                case AcseServiceUser.AUTHENTICATION_REQUIRED:
                    c.reply.clear()
                    c.getApplicationAssociationRequest()
                    await c.read_data_block()
                    c.parseApplicationAssociationResponse()
                case _ as diagnostic:
                    raise exc.AssociationResultError(diagnostic)
            c.set_error(Transmit.OK, "Initialize connection")
            # TODO: remove DIMA crutch dummy read for correct write
            if c.objects is not None:
                c.get_get_request_normal(c.objects.LDN.get_attr_descriptor(2))
                await c.read_data_block()
                c.matching_LDN(octet_string.LDN(c.reply.data.get_data()))
        return await self.exchange(c)

    @abstractmethod
    async def exchange(self, c: Client):
        """application level exchange"""


class Dummy(ExTask):
    """dummy task"""

    async def exchange(self, c: Client):
        """"""
        c.log(logL.INFO, "dummy task")


@dataclass
class Loop(ExTask):
    task: ExTask
    func: Callable[[Any], bool]
    delay: int
    attempt_amount: int = 0
    """0 is never end loop"""

    async def run(self, c: Client):
        attempt = count()
        while not self.func(await super(Loop, self).run(c)):
            if next(attempt) == self.attempt_amount:
                return False
            await asyncio.sleep(self.delay)
        return True

    async def exchange(self, c: Client):
        return await self.task.exchange(c)


class Sequence(ExTask):
    """for exchange task sequence"""
    tasks: list[ExTask]
    __is_exchange: bool

    def __init__(self, *tasks: ExTask):
        assert all((isinstance(t, ExTask) for t in tasks))
        self.tasks = list(tasks)
        self.__is_exchange = False

    def append(self, task: ExTask):
        if not self.__is_exchange:
            self.tasks.append(task)
        else:
            raise RuntimeError(F"append to {self.__class__.__name__} not allowed, already exchange started")

    async def exchange(self, c: Client) -> list[cdt.CommonDataType | None]:
        ret = list()
        self.__is_exchange = True
        for t in self.tasks:
            # ret.append(await t.exchange(c))
            # TODO: remove in future try-except block with pleasure return value => ret.append(await t.exchange())
            try:
                res = await t.exchange(c)
            except exc.ResultError as e:
                res = e
            ret.append(res)
        return ret


class FindServerVersion(ExTask):
    """try find COSEM server version, return: instance(B group), CDT"""

    async def exchange(self, c: Client) -> tuple[int, cdt.CommonDataType]:
        for desc in (ut.CosemAttributeDescriptor((1, "0.0.0.2.1.255", 2)), ut.CosemAttributeDescriptor((1, "0.0.96.1.2.255", 2))):
            try:
                return desc.instance_id.contents[1], cdt.get_instance_and_pdu_from_value(await c.read_attr(desc))[0]
            except exc.ResultError as e:
                if e.result == pdu.DataAccessResult.OBJECT_UNDEFINED:
                    """try search in old object and set to new"""
                    continue
                else:
                    raise e
        else:
            raise exc.NoObject(F"not find version object in server")


class InitType(ExTask):
    """nothing params"""
    # async def exchange(self, c: Client, is_public: bool = False):
    #     await c.close()  # close hdlc before init
    #     return await super(InitType, self).exchange(c, is_public=True)

    async def exchange(self, c: Client) -> bool:
        # read LDN
        data = await c.read_attr(collection.AttrDesc.LDN_VALUE)
        ldn = octet_string.LDN(data)
        # find device_id(type for Russia)
        type_value, _ = cdt.get_instance_and_pdu_from_value(await c.read_attr(ut.CosemAttributeDescriptor((1, "0.0.96.1.1.255", 2))))
        ver_inst, ser_ver_cdt = await FindServerVersion().exchange(c)
        ser_ver = AppVersion.from_str(ser_ver_cdt.to_str())  # todo: handle not SemVer
        try:
            c.objects = collection.get_collection(
                manufacturer=ldn.manufacturer(),
                server_type=type_value,
                server_ver=ser_ver)
            c.objects.LDN.set_attr(2, ldn)
        except exc.NoConfig as e:
            c.log(logL.WARN, F"false init type procedure: {e}, start create objects from device")
            new_collection = collection.Collection(ldn=ldn)
            new_collection.set_server_type(type_value)  # if xml file not contains the type
            # read association
            object_list: cdt.Array = cdt.Array(await c.read_attr(collection.AttrDesc.OBJECT_LIST), type_=structs.ObjectListElement)
            for c_id, ver, ln, _ in object_list:
                new_obj = new_collection.add_if_missing(  # todo: remove add_if
                    class_id=ut.CosemClassId(int(c_id)),
                    version=ver,
                    logical_name=ln)
                if new_obj.CLASS_ID == overview.ClassID.ASSOCIATION_LN:  # search association for keep object_list into
                    await c.read_attr(new_obj.get_attr_descriptor(3))
                    if new_obj.associated_partners_id.client_SAP == c.SAP:
                        new_obj.set_attr(2, object_list)
            new_collection.get_class_version()
            c.objects = new_collection
            # read all DeviceIDObjects
            for d_id in collection.get_filtered(
                objects=c.objects,
                keys=(
                    ln_pattern.DEVICE_IDS,
                    ln_pattern.PROGRAM_ENTRIES)):
                await c.read_attribute(d_id, 2)

            # TODO: handle 6.2.42 DLMS UA 1000-1 Ed. 14 - Device ID objects, 6.2.4 Other abstract general purpose OBIS codes(Program entries for version)
            # TODO: keep in Types
        c.objects.set_server_ver(
            instance=ver_inst,
            value=ser_ver)
        c.log(logL.INFO, F"added {len(c.objects)} DLMS objects")
        return True


@dataclass
class ReadAttribute(ExTask):
    ln: collection.LNContaining
    index: int

    async def exchange(self, c: Client) -> cdt.CommonDataType:
        # TODO: check is_readable
        obj = c.objects.get_object(self.ln)
        return await self.read_from_obj(c, obj, self.index)

    @staticmethod
    async def read_from_obj(c: Client, obj: collection.InterfaceClass, index: int) -> cdt.CommonDataType | ValueError:
        c.get_get_request_normal(
            attr_desc=obj.get_attr_descriptor(
                value=index,
                with_selection=bool(c.negotiated_conformance.selective_access)))
        start_read_time: float = time.perf_counter()
        await c.read_data_block()
        c.last_transfer_time = datetime.timedelta(seconds=time.perf_counter()-start_read_time)
        try:
            obj.set_attr(index, c.reply.data.get_data())
            return obj.get_attr(index)
        except ValueError as e:
            return e


@dataclass
class ReadEmptyAttribute(ExTask):
    """read if attribute is empty"""
    ln: collection.LNContaining
    index: int

    async def exchange(self, c: Client):
        # TODO: check is_readable
        if c.objects.get_object(self.ln).get_attr(self.index) is None:
            data = await ReadAttribute(
                ln=self.ln,
                index=self.index).exchange(c)


@dataclass
class ReadAttributes(ExTask):
    ln: collection.LNContaining
    indexes: tuple[int, ...]

    async def exchange(self, c: Client) -> tuple[cdt.CommonDataType | ValueError]:
        obj = c.objects.get_object(self.ln)
        ret: list[cdt.CommonDataType | ValueError] = list()
        # TODO: check for Get-Request-With-List
        for i in self.indexes:
            ret.append(await ReadAttribute.read_from_obj(c, obj, i))
        return tuple(ret)


@dataclass
class WriteAttribute(ExTask):
    ln: collection.LNContaining
    index: int
    value: bytes | str | int | list | tuple | datetime.datetime

    async def exchange(self, c: Client):
        obj = c.objects.get_object(self.ln)
        if isinstance(self.value, (str, int, list, tuple, datetime.datetime)):
            value2 = await c.encode(
                obj=obj,
                index=self.index,
                value=self.value)
            enc = value2.encoding
        else:
            enc = self.value
        data = c.get_set_request_normal(
            obj=obj,
            attr_index=self.index,
            value=enc)
        return await c.read_data_block()


@dataclass
class WriteAttributesOld(ExTask):
    """todo: use for write without value(from object) replace all to WriteAttribute in future."""
    ln: collection.LNContaining
    indexes: tuple[int, ...]

    async def exchange(self, c: Client):
        for i in self.indexes:
            if c.objects.is_writable(
                    ln=(obj := c.objects.get_object(self.ln)).logical_name,
                    index=i,
                    association_id=c.objects.get_association_id(c.SAP)):
                data = c.get_set_request_normal(
                    obj=obj,
                    attr_index=i)
                await c.read_data_block()
            else:
                raise exc.ITEApplication(F"Access Error. From current association: {obj}: {i} is not writable")


@dataclass
class ExecuteByDesc(ExTask):
    """execute method by method descriptor # TODO: rewrite this"""
    desc: ut.CosemMethodDescriptor

    async def exchange(self, c: Client):
        try:
            await c.execute_method(self.desc)
            c.set_error(Transmit.OK, F'Execute {self.desc}.')
        except Exception as e:
            c.log(logL.INFO, F'ERROR: Исполнение {self.desc}')
            c.set_error(Transmit.EXECUTE_ERROR, F'Исполнение {self.desc}')


@dataclass
class Execute(ExTask):
    """execute method by method descriptor # TODO: rewrite this with <value>"""
    ln: collection.LNContaining
    index: int
    value: str

    async def exchange(self, c: Client):
        obj = c.objects.get_object(self.ln)
        try:
            await c.execute_method(ut.CosemMethodDescriptor(
                (obj.CLASS_ID,
                 ut.CosemObjectInstanceId(obj.logical_name.contents),
                 ut.CosemObjectMethodId(self.index))
            ))
            c.set_error(Transmit.OK, F'Execute {self.ln}: {self.index}.')
        except Exception as e:
            c.log(logL.INFO, F'ERROR: Исполнение {self.ln}: {self.index}')
            c.set_error(Transmit.EXECUTE_ERROR, F'Исполнение {self.ln}: {self.index}')


class WriteTime(ExTask):
    """write Clock.time depend from transfer time"""

    async def exchange(self, c: Client):
        try:
            obj = c.objects.clock
            c.get_get_request_normal(obj.get_attr_descriptor(3))
            await c.read_data_block()
            tz = obj.get_attr_element(3).DATA_TYPE(c.reply.data.get_data())
            await WriteAttribute(
                ln=obj.logical_name,
                index=2,
                value=(datetime.datetime.utcnow() + datetime.timedelta(minutes=tz.decode()) + c.last_transfer_time)
            ).exchange(c)
            # obj.set_attr(2, (cst.OctetStringDateTime(datetime.datetime.utcnow() + datetime.timedelta(minutes=obj.time_zone.decode()) + dev.last_transfer_time)))
            # dev.write_attr(obj, 2)
            # logger.info(F'Write attribute: 2 success')
            c.errors[Transmit.OK] = 'Запись времени'
        except Exception as e:
            # logger.info(F'ERROR: write Clock: attribute 2 {e}')
            c.errors[Transmit.WRITE_ERROR] = F"write time: {e}"

# @dataclass
# class UpdateResponse:
#     result:


@dataclass
class Progress(State):
    position: int
    max: int
    message: str

    def __str__(self):
        return F"{self.message}: {self.position}/{self.max}"


@dataclass
class UpdateFirmware(ExTask):
    """only for KPZ now"""

    async def exchange(self, c: Client) -> bool:
        read_seq = Sequence()
        match c.objects.collection_ver:
            case AppVersion(0, 0, patch) if 25 <= patch < 26:
                read_seq.append(ReadAttribute(
                    ln=c.objects.firmwares_description.logical_name,
                    index=2))
                read_seq.append(ReadAttribute(
                    ln=c.objects.firmware_version.logical_name,
                    index=2))
                read_seq.append(ReadAttribute(
                    ln=c.objects.firmware_image_transfer.logical_name,
                    index=2))
            case AppVersion(0, 0, patch) if 26 <= patch <= 52:  # to max available version
                read_seq.append(ReadAttribute(
                    ln=c.objects.firmwares_description.logical_name,
                    index=2))
                read_seq.append(ReadAttribute(
                    ln=c.objects.firmware_version.logical_name,
                    index=2))
                read_seq.append(ReadAttribute(
                    ln=c.objects.firmware_image_transfer.logical_name,
                    index=2))
                read_seq.append(ReadAttribute(
                    ln=c.objects.boot_image_transfer.logical_name,
                    index=2))
            case AppVersion(0, 0, 53) | AppVersion(1, 1 | 2 | 3) | AppVersion(1, 4, 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7):  # to max available version
                read_seq.append(ReadAttribute(
                    ln=c.objects.firmwares_description.logical_name,
                    index=2))
                read_seq.append(ReadAttribute(
                    ln=c.objects.firmware_version.logical_name,
                    index=2))
                read_seq.append(ReadAttributes(
                    ln=c.objects.firmware_image_transfer.logical_name,
                    indexes=(2, 6)))
                read_seq.append(ReadAttribute(
                    ln=c.objects.boot_image_transfer.logical_name,
                    index=2))
            case AppVersion(1, 4 | 5 | 6 | 7):  # to max available version
                read_seq.append(ReadAttribute(
                    ln=c.objects.firmwares_description.logical_name,
                    index=2))
                read_seq.append(ReadAttributes(
                    ln=c.objects.firmware_image_transfer.logical_name,
                    indexes=(2, 6)))
                read_seq.append(ReadAttribute(
                    ln=c.objects.boot_image_transfer.logical_name,
                    index=2))
            case AppVersion(0, 0, 0) | AppVersion(-1):
                c.set_error(Application.VERSION_ERROR, 'Unknown metrology Version')
                return False
            case AppVersion():
                c.set_error(Application.VERSION_ERROR, F'Version {c.objects.server_ver} don\'t read update properties')
                return False
            case _:
                c.set_error(Transmit.READ_ERROR, 'Wrong AppVersion')
                return False
        # add optional object if its values absence
        ret = await read_seq.exchange(c)
        for r, t in zip(ret, read_seq.tasks):
            if isinstance(r, exc.ResultError):  # todo: rewrite with new ReadResponse
                c.set_error(Transmit.READ_ERROR, message=F"error in {t}: {r}")
                return False
        c.objects.firmware_image_transfer.clear_image()  # TODO: check for missing objects !!
        firmwares_description_obj = c.objects.firmwares_description
        boot_version: int = int(firmwares_description_obj.value.decode()[:4])
        firmwares_description = firmwares_description_obj.value.decode()[4:]
        suitable_firmware: AppVersion = AppVersion(0, 0, 1)
        suitable_boot: int = 0
        temp_key: tuple | None = None
        """ key of image for update """
        if not (firms := get_firmware(manufacturer := c.objects.manufacturer)):
            c.log(logL.ERR, F"not find firmwares for {manufacturer=}")
            return False  # not find
        firmwares, boots = firms
        # search firmware image
        for key in firmwares:
            match key:
                case (int(), int(), int()) as app_args, str() as desc:
                    match compare_version := AppVersion(*app_args):
                        case AppVersion(0) if firmwares_description in desc:
                            """good"""
                        case AppVersion(1, minor) if minor <= 2 and firmwares_description in desc:
                            """good"""
                        case AppVersion(1, minor) if (minor in (3, 4, 5, 6, 7)) and desc.split("_", maxsplit=5)[1:5] == firmwares_description.split("_", maxsplit=5)[:4]:
                            """good"""
                        case AppVersion(0 | 1, minor) if minor <= 7:
                            continue
                        case error:
                            c.log(logL.ERR, F"Неизвестная версия ПО: {error}")
                            return False
                case error_key_type:
                    c.log(logL.ERR, F"Неизвестный тип {error_key_type} в *.dat файле")
                    return False
            if compare_version > suitable_firmware:
                suitable_firmware = compare_version
                temp_key = key
        if suitable_firmware != c.objects.server_ver[0] and temp_key is not None:
            image: bytes = firmwares.get(temp_key)
            c.objects.firmware_image_transfer.set_image_for_update(
                value=image,
                identifier=bytearray(hashlib.md5(image).digest()))
            c.log(logL.INFO, F"set image to update {suitable_firmware=}")
        else:
            c.log(logL.INFO, F"{c.objects.server_ver[0]=} is actual")
        # search boot image
        temp_key = None
        for key in boots:
            match key:
                case 1 | 2 | 3 | 4 | 5 | 6 as compare_version, desc if firmwares_description in desc:
                    """good"""
                case 7 | 8 | 9 | 10 | 11 | 12 | 13 as compare_version, desc if desc.split("_", maxsplit=5)[1:5] == firmwares_description.split("_", maxsplit=5)[:4]:
                    """good"""
                # case 9 | 10 as invalid:
                #     messagebox.showerror("Внутренняя ошибка", F"Невалидная версия загрузчика {invalid}")
                case int() as version, _ if version <= 13:
                    continue
                case error:
                    c.log(logL.ERR, F"Неизвестная версия загрузчика {error[0]}")
                    return False
            if compare_version > suitable_boot:
                suitable_boot = compare_version
                temp_key = key
        c.objects.boot_image_transfer.clear_image()
        if suitable_boot != boot_version and temp_key is not None:
            image: bytes = boots.get(temp_key)
            c.objects.boot_image_transfer.set_image_for_update(
                value=image,
                identifier=bytearray(hashlib.md5(image).digest()))
            c.log(logL.INFO, F"set image to update {suitable_boot=}")
        else:
            c.log(logL.INFO, F"{boot_version=} is actual")

        # update
        match c.objects.server_ver[0]:
            case AppVersion(0, 0, 53 | 54) | AppVersion(1, 1 | 2 | 3 | 4 | 5 | 6):
                if await self.__is_updated_image_3(c=c, obj=c.objects.boot_image_transfer):
                    await ReadAttribute(
                        ln=c.objects.firmwares_description.logical_name,
                        index=2).exchange(c)
                    res = await self.__is_updated_image_3(c=c, obj=c.objects.firmware_image_transfer)
                else:
                    return False
            case AppVersion(0, 0, patch) if 48 <= patch <= 52:
                if await self.__is_updated_image_2(c=c, obj=c.objects.boot_image_transfer):
                    await ReadAttribute(
                        ln=c.objects.firmwares_description.logical_name,
                        index=2
                    ).exchange(c)
                    res = await self.__is_updated_image_2(c=c, obj=c.objects.firmware_image_transfer)
                else:
                    return False
            case AppVersion(0, 0, patch) if 39 <= patch <= 47:
                if await self.__is_updated_image(c=c, obj=c.objects.boot_image_transfer):
                    await ReadAttribute(
                        ln=c.objects.firmwares_description.logical_name,
                        index=2
                    ).exchange(c)
                    res = await self.__is_updated_image(c=c, obj=c.objects.firmware_image_transfer)
                else:
                    return False
            case AppVersion(0, 0, patch) if 25 <= patch <= 38:
                res = await self.__is_updated_image(c=c, obj=c.objects.firmware_image_transfer)
            case AppVersion(0, 0, 0):
                c.set_error(Transmit.EXECUTE_ERROR, F'Не могу установить номер версии счетчика')
                return False
            case AppVersion():
                c.set_error(Transmit.EXECUTE_ERROR, F'Невозможно обновить версию {c.objects.server_ver}')
                return False
            case _:
                return False
        return await InitType().exchange(c)

    async def __is_updated_image(self, c: Client, obj: collection.ImageTransfer) -> bool:
        """ update image if blocks is fulls """
        if obj.is_image_exist:
            c.current_obj = obj
            try:
                await c.execute_method(obj.get_meth_descriptor(1))
                c.log(logL.INFO, "Start initiate Image Transfer")
                while True:
                    if c.is_stop_request:
                        c.set_error(Transmit.ABORT, '')
                        return False
                    await c.execute_method(obj.get_meth_descriptor(2))
                    c.log(logL.INFO, F"start block: {obj.current_block_transfer=} transferred")
                    try:
                        obj.set_next_block()
                    except StopIteration:
                        c.log(logL.INFO, "All blocks transferred")
                        break
                await c.execute_method(obj.get_meth_descriptor(4))  # attention without verification
                c.log(logL.INFO, "Start Activate Transfer")
                return True
            except Exception as e:
                c.log(logL.ERR, F'unhandled update error. {e.args[0]}')
                return False
        else:
            return True

    async def __is_updated_image_2(self, c: Client, obj: collection.ImageTransfer) -> bool:
        """ update image if blocks is fulls ver 2"""
        if obj.is_image_exist:
            is_activating: bool = False
            c.current_obj = obj
            try:
                # TODO: copypast from __is_updated_image_3
                await ReadAttributes(
                    ln=obj.logical_name,
                    indexes=(6, 7)
                ).exchange(c)
                if obj.image_transfer_status in (i_t_status.TRANSFER_NOT_INITIATED, i_t_status.VERIFICATION_FAILED, i_t_status.ACTIVATION_FAILED) \
                        or len(obj.image_to_activate_info) == 0 \
                        or obj.image_to_activate_info[0].image_to_activate_identification != obj.image_transfer_initiate.image_identifier:
                    await c.execute_method(obj.get_meth_descriptor(1))
                    c.log(logL.INFO, "Start initiate Image Transfer")
                    obj.set_block_for_transfer(0)
                else:
                    c.log(logL.INFO, "already INITIATED")
                    await ReadAttribute(
                        ln=obj.logical_name,
                        index=4
                    ).exchange(c)
                    try:
                        block_number = int(obj.image_first_not_transferred_block_number)
                        obj.set_block_for_transfer(block_number if block_number != 1 else 0)  # bag in SERVER: always start from 1
                    except IndexError:
                        """pass. not set"""
                # END copypast
                while True:
                    if c.is_stop_request:
                        c.set_error(Transmit.ABORT, '')
                        return False
                    await c.execute_method(obj.get_meth_descriptor(2))
                    c.log(logL.INFO, "start block: {obj.current_block_transfer=} transferred")
                    try:
                        obj.set_next_block()
                    except StopIteration:
                        c.log(logL.INFO, "All blocks transferred")
                        break
                await c.execute_method(obj.get_meth_descriptor(4))
                c.log(logL.INFO, "Start Activate Transfer. Timeout 22 second. Waiting verification")
                time.sleep(22)
                is_activating = False
                c.set_error(Transmit.ABORT, F'Expected device Reboot')
                c.set_error(Application.OK, F'Activated')
                return True
            except Exception as e:
                c.set_error(Transmit.EXECUTE_ERROR, F'{e.args[0]}')
                return False
            finally:
                if is_activating:
                    c.set_error(Transmit.EXECUTE_ERROR, 'Activating')
                c.current_obj = None
        else:
            return True

    async def __is_updated_image_3(self, c: Client, obj: collection.ImageTransfer) -> bool:
        """ update image if blocks is fulls ver 3"""
        if obj.is_image_exist:
            # TODO: need common counter for exit from infinity loop
            c.current_obj = obj
            previous_status: i_t_status.ImageTransferStatus | None = None
            await ReadAttributes(
                ln=obj.logical_name,
                indexes=(6, 7)
            ).exchange(c)
            current_status = obj.image_transfer_status
            if obj.image_transfer_status in (i_t_status.TRANSFER_NOT_INITIATED, i_t_status.VERIFICATION_FAILED, i_t_status.ACTIVATION_FAILED) \
                    or len(obj.image_to_activate_info) == 0 \
                    or obj.image_to_activate_info[0].image_to_activate_identification != obj.image_transfer_initiate.image_identifier:
                await c.execute_method(obj.get_meth_descriptor(1))
                c.log(logL.INFO, "Start initiate Image Transfer")
                await ReadAttribute(
                    ln=obj.logical_name,
                    index=6
                ).exchange(c)
            elif obj.image_transfer_status == i_t_status.ACTIVATION_SUCCESSFUL:
                # image in outside memory and already activated early, but erased by hard programming. Need again go to activation
                obj.image_transfer_status.set(i_t_status.VERIFICATION_SUCCESSFUL)
            else:
                c.log(logL.INFO, "already INITIATED")
                await ReadAttribute(
                    ln=obj.logical_name,
                    index=4
                ).exchange(c)
                try:
                    obj.set_block_for_transfer(int(obj.image_first_not_transferred_block_number))
                except IndexError as e:  # Skip set block
                    await c.execute_method(obj.get_meth_descriptor(3))
                    c.log(logL.INFO, "Start Verify Transfer")
            while True:
                c.log(logL.STATE, F"{obj.get_attr_element(6)}: {obj.image_transfer_status}")
                try:
                    match current_status:
                        case i_t_status.VERIFICATION_FAILED if current_status == previous_status:
                            c.set_error(Application.VERIFY_ERROR, 'Twice ERROR')
                            return False
                        case i_t_status.TRANSFER_INITIATED if current_status == previous_status:
                            c.set_error(Application.VERIFY_ERROR, F"Expected Switch to Verification Initiated status, got Initiated")
                        case i_t_status.TRANSFER_NOT_INITIATED:
                            c.set_error(Application.ACTIVATION_ERROR, 'Got Not initiated status after call Initiation')
                        case i_t_status.TRANSFER_INITIATED:
                            while True:
                                if c.is_stop_request:
                                    c.set_error(Transmit.ABORT, '')
                                    return False
                                await c.execute_method(obj.get_meth_descriptor(2))  # start block: {obj.current_block_transfer} transferred
                                try:
                                    c.log(logL.STATE, Progress(obj.current_block_transfer, obj.get_n_blocks(), F"{obj.get_meth_element(2)}"))
                                    obj.set_next_block()
                                except StopIteration:
                                    c.log(logL.INFO, "All blocks transferred")
                                    break
                            await c.execute_method(obj.get_meth_descriptor(3))  # Start Verify Transfer
                        case i_t_status.VERIFICATION_INITIATED:
                            c.log(logL.INFO, "read bitstring. It must grow")
                            # TODO: calculate time for waiting or read growing bitstring ?
                            await ReadAttribute(
                                ln=obj.logical_name,
                                index=3
                            ).exchange(c)
                            if len(obj.image_transferred_blocks_status) < int(obj.image_block_transfer.image_block_number):
                                c.log(logL.INFO, F"Got blocks[{len(obj.image_transferred_blocks_status)}]: {obj.image_transferred_blocks_status}")
                            else:
                                c.log(logL.INFO, "All Bits solved")
                        case i_t_status.VERIFICATION_FAILED:
                            await ReadAttribute(
                                ln=obj.logical_name,
                                index=3
                            ).exchange(c)
                            valid = obj.image_transferred_blocks_status.decode()
                            c.log(logL.INFO, F"Got blocks[{len(obj.image_transferred_blocks_status)}]: {obj.image_transferred_blocks_status}")
                            log_state = Progress(0, obj.get_n_blocks(), F"{collection.get_name(obj.logical_name)}")
                            c.log(logL.STATE, log_state)
                            for index in filter(lambda it: valid[it] == 0, range(len(valid))):
                                obj.set_block_for_transfer(index)
                                await c.execute_method(obj.get_meth_descriptor(2))
                                if isinstance(c.state, Progress):
                                    log_state.position = index
                                    c.log(logL.STATE, log_state)
                                # c.log(logL.INFO, F"start block: {obj.current_block_transfer} transferred")
                            await c.execute_method(obj.get_meth_descriptor(3))
                            c.log(logL.INFO, "Start Verify Transfer")
                        case i_t_status.VERIFICATION_SUCCESSFUL:
                            await ReadAttributes(
                                ln=obj.logical_name,
                                indexes=(7, 4, 3)
                            ).exchange(c)
                            valid = obj.image_transferred_blocks_status.decode()
                            c.log(logL.INFO, F"md5:{obj.image_to_activate_info[0].image_to_activate_signature}")
                            if any(map(lambda it: it == 0, valid)):
                                c.set_error(Application.VERIFY_ERROR, 'Exist 0 blocks')
                                await c.execute_method(obj.get_meth_descriptor(1))
                                c.log(logL.INFO, "Start initiate Image Transfer, after wrong verify. Exist 0 blocks")
                                return False
                            elif int(obj.image_first_not_transferred_block_number) < len(valid):
                                c.set_error(Application.VERIFY_ERROR, F'Got {obj.image_first_not_transferred_block_number} not transferred block')
                                await c.execute_method(obj.get_meth_descriptor(1))
                                c.log(logL.INFO, "Start initiate Image Transfer, after wrong verify. Got not transferred block")
                                return False
                            elif obj.image_to_activate_info[0].image_to_activate_signature != obj.image_to_activate_info[0].image_to_activate_identification:
                                message: str = F"Signature not match to Identification: got {obj.image_to_activate_info[0].image_to_activate_signature}, " \
                                               F"expected {obj.image_to_activate_info[0].image_to_activate_identification}"
                                c.set_error(Application.VERIFY_ERROR, message)
                                await c.execute_method(obj.get_meth_descriptor(1))
                                c.log(logL.INFO, F"Start initiate Image Transfer, after wrong verify. {message}")
                                return False
                            else:
                                await c.execute_method(obj.get_meth_descriptor(4))
                                c.log(logL.INFO, "Start Activate Transfer")
                        case i_t_status.ACTIVATION_INITIATED:
                            c.set_error(Application.OK, F'Activated')
                            await c.disconnect_request()
                            time.sleep(5)
                            return True
                        case i_t_status.ACTIVATION_SUCCESSFUL:
                            await ReadAttribute(
                                ln=obj.logical_name,
                                index=7
                            ).exchange(c)
                            if obj.image_to_activate_info[0].image_to_activate_identification == obj.image_transfer_initiate.image_identifier:
                                c.set_error(Application.OK, F'Activated')
                                c.log(logL.INFO, "already activated this image")
                                return True
                            else:
                                await c.execute_method(obj.get_meth_descriptor(1))
                                c.log(logL.INFO, "Start initiate Image Transfer")
                                # TODO: need wait clearing memory in device ~5 sec
                        case i_t_status.ACTIVATION_FAILED:
                            c.set_error(Application.ACTIVATION_ERROR, 'Ошибка активации...')
                            return False
                        case _: raise exc.DLMSException('Unknown image transfer status')
                    previous_status = current_status
                except Exception as e:
                    c.set_error(Transmit.EXECUTE_ERROR, F'{e.args[0]}')
                    return False
                finally:
                    c.current_obj = None
                time.sleep(1)  # TODO: tune it
                await ReadAttribute(
                    ln=obj.logical_name,
                    index=6
                ).exchange(c)
        else:
            return True


class TestAll(ExTask):
    """read all attributes with check access"""  # todo: add Write with access

    async def exchange(self, c: Client):
        if await InitType().exchange(c):
            ass: collection.AssociationLN = c.objects.getAssociationBySAP(c.SAP)
            for obj in tuple(c.objects):
                indexes: list[int] = [i for i, _ in obj.get_index_with_attributes()]
                attempt = count(1)
                while True:
                    c.log(logL.INFO, F"start read {obj} attr: {', '.join(map(str, indexes))}. attempt={next(attempt)}")
                    len_indexes: int = len(indexes)
                    for i in tuple(indexes):
                        try:
                            is_readable = ass.is_readable(
                                ln=obj.logical_name,
                                index=i)
                            res = await ReadAttribute(
                                ln=obj.logical_name,
                                index=i
                            ).exchange(c)
                            if not is_readable:
                                c.log(logL.ERR, F"{obj} with attr={i} must be unreadable")
                            indexes.remove(i)
                            c.log(logL.INFO, F"Get {obj}:{obj.get_attr_element(i)}")
                            if isinstance(res, ValueError):
                                c.log(logL.WARN, F"ValueError. For {obj} attr:{i} {res}")
                        except exc.ResultError as e:
                            if e.result == pdu.DataAccessResult.READ_WRITE_DENIED and not is_readable:
                                c.log(logL.INFO, F"success ReadAccess TEST: {e}")
                                indexes.remove(i)
                            else:
                                c.log(logL.ERR, F"result_error {e}")
                        except exc.ITEApplication as e:
                            c.log(logL.ERR, F"ITEApplication. For {obj} attr:{i} {e}")
                        except Exception as e:
                            c.log(logL.ERR, F"Unknown. For {obj} attr:{i} {e}")
                    if len(indexes) == 0:
                        c.log(logL.INFO, "all read success")
                        break
                    elif len(indexes) == len_indexes:
                        c.log(logL.ERR, F"can't read attr={', '.join(map(str, indexes))}")
                        break
                    else:
                        c.log(logL.WARN, F"has a errors in attr={', '.join(map(str, indexes))}. Need more attempt")
                # todo: check write problem - if send_frame clear then counter is wrong, need fix in client it
            return True

