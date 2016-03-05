import kl_http,kl_db,os,json,kl_log,kl_reg
regex=kl_reg
db=kl_db.mysql({
            'host':'localhost',
            'user':'root',
            'passwd':'adminrootkl',
            'db':'qiche',
            'prefix':'kl_',
            'charset':'utf8'
        })
http=kl_http.kl_http()
log=kl_log.kl_log('brand')


http.setheaders('''\
Content-Type:application/x-www-form-urlencoded
Host:www.epicc.com.cn
Origin:http://www.epicc.com.cn
Referer:http://www.epicc.com.cn/ecar/proposal/normalProposal
User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36
X-Requested-With:XMLHttpRequest\
''')
#取承保验证码
url='http://www.epicc.com.cn/ecar/proposal/normalProposal'
postdata='''\
areaCode:41000000
cityCode:41010000
cityCodeLast:41010000
IKType:01
Preview:0
InterNo:/
Simulation:true
xubao:0
threeZuheFlag:0
threeZuhe:0
isnewcar:1
licenseno:豫*
isRenewal:0\
'''
prpcmainuniqueID=''
r=http.posturl(url,postdata)
if not http.lasterror:
    content=r.read().decode()
    idreg='<input.*?name\=\"prpcmain\.uniqueID\".*?value\=\"(.*?)\".*?>'
    mat=regex.findall(idreg,content)
    prpcmainuniqueID=mat[0]
    print(mat[0])

#第一次验证
postdata='''\
eadinsuredInfoTrandata:
eadinsuredInfoZ:
eadinsuredInfoTrandataZ:
zIsOnlyInsure:
zcopies:
zcountInsred:
eadThreeStepFlagZ:
carOwnerRemind:
majorFactoryFm:
lastCiEndDate:
hzPolicy:
cooperator:
tbOrderNo:
cooperatorFlag:false
telContact:1
onlineService:1
appCallback:1
wangyiCon:1
faq:1
reinsurance:
sendPrice:1
savePrice:1
carPeopleAccident:1
VIPFlag:
prpemployeeUserid:
pin:
pazxData:
haocheData:
mobilePhone:
provinceCode:
prpcmain.areaCode:41000000
prpcmain.areaCodeLast:41000000
prpcmain.cityCode:41010000
prpcmain.cityCodeLast:41010000
prpcitemCar.licenseno:008558
newCarEnableFlag_stepone:1
oldPolicyNo:
entryId:
ccaEntryId:
prpcmain.comcode:41010088
prpcmain.makecom:41010088
prpcmain.handlercode:4101880120
prpcmain.handler1code:4101880120
prpcmain.handler1code_uni:1241010107
prpcmain.handlercode_uni:1241010107
prpcmain.operatorcode:4101880120
branchcode:41010000
cityName:郑州
provinceName:河南
threeZuheFlag:0
threeZuhe:0
checkBZDate:
isrenewalonlycar:1
checkcode:
lastcarownername:
comcname:郑州
priceConfigKind:2
prpcmain.uniqueID:[prpcmain.uniqueID]
deliverAddressFlag:1
serverDateTime:2016/3/2 10:02
userPriceConf:1
BM_flag:0
countyName:
oldinterimno:
TZFlag:
isblackFlag:
ccaEntryLinks:
ccaID:
ccaFlag:
toPageProposalZJson:
ccaemail:
itemKindFlag:caculateInfo
zancunmail:0
baojiaflag:0
taxEnable:1
BISigle:1
BZSigle:1
zSameAsFlag:000
quotepriceFlag:
phoneVerificationflag:0
driveAreaName:河南省内行驶
tokenNo:
frameNoBJ:
engineNoBJ:
carOwnerBJ:
renewalRand:
quickPrice:
prpcmain.renewal:2
agentTypeValue:
pos:
carInfoPos:
carInfoFromMyins:
CarModelType:
prpcitemCar.modelcode:DZABJD0007
prpcitemCar.purchaseprice:176900
isOutRenewal:0
lastHas050200:0
lastHas050500:0
lastHas050210:0
lastHas050310:0
lastHas050291:0
mrPurchasePrice:176900
oriPurchasePrice:192000
purchasePriceMin:123830
purchasePriceMax:229970
DQAmountMin:
DQAmountMax:
DQAmount:
purchasePriceByDeclinature:
nbCheckFlag:
prpcitemCar.countrynature:03
prpcitemCar.useyears:0
newCarMonths:12
prpcitemCar.licenseflag:0
prpcitemCar.newCar_check:on
prpcitemCar.newcarflag:0
prpcitemCar.carloanflag:0
prpcitemCar.transfervehicleflag:0
prpcitemCar.nonlocalflag:0
marketYear:
TonCount:
isHBpriceconfig:0
returnCarModelJson:
returnCarModelJsonTemp:
returnRenewalJson:
returnERiskJson:
beforeProposalNo:
renewalPackage:renewalPackage
hasRealTime:0
seatCountOri:5
queryPostCodeCity:
prpcinsureds[1].insurednature:3
prpcinsureds[1].:1
prpcinsureds[0].insuredflag:0010000
prpcinsureds[1].insuredflag:1000000
prpcinsureds[2].insuredflag:0100000
prpcinsureds[0].postcode:
prpcinsureds[0].insuredaddress:
renewalAppMobile:
BZ_timeChangeFlag:0
BI_timeChangeFlag:0
EnrollDateyc:1
returnNonRenewal:
tn_identityId:
cmpid:
carOwnerChangeFlag:0
prpcmain.changeFlag_renewal:0
packageFromQuick:
cooperatorFlag:false
prpcmain.packageName:EconomyPackage
prePackageName:
isNeedQueryCarModel:0
carInfoChangeFlag:1
StartDateJQ_renewal:
StartHourJQ_renewal:
guohutishi:0
nodamyearsBi:
purchasePrice_renewal:0
jyFlag:
jyType:
jyIcon:
jyBrandId:
jyFamilyId:
jyGroupId:
jyParentId:
jyParentName:
jyGearboxType:
jyImportFlag:1
showSeatCountFlag:
jyGroupPicData:/home/ecar/jy/pics/group/DZA2AH01/small/small_DZA2AH01_1.jpg,/home/ecar/jy/pics/group/DZA2AH01/small/small_DZA2AH01_2.jpg,/home/ecar/jy/pics/group/DZA2AH01/small/small_DZA2AH01_3.jpg
jyBrandPicData:
prpcitemCar.runmiles:10000
prpcitemCarext.nodamyearsbi:0
prpcmain.xzlastdamagedbi:0
oldframeno:
oldengineno:
prpcitemCar.frameno:LGXC16AF5G0008558
isFocus:0
prpcitemCar.vinno:LGXC16AF5G0008558
prpcitemCar.engineno:216005190
prpcitemCar.enrolldate:2016/03/02
prpcitemCar.brandname:大众汽车SVW71816EU
jyBrandName:
jyGroupName:请选择
jyDisplacement:请选择
jyGearboxName:请选择
jyParentVehName:请选择
jyFgwCode:请选择
prpcitemCar.aliasname:
prpcitemCar.seatcount:5
prpcmain.startdate:2016/03/03
prpcmain.starthour:0
prpcmain.enddate:2017/03/02
prpcmain.endhour:24
startDateBI:2016/03/03
starthourBI:0
endDateBI:2017/03/02
endhourBI:24
StartDateBIpro:24
endDateBIpro:24
startDateisChanged:0
prpcitemCar.TravelMilesvalue:1
guohuselect:0
prpcitemCar.transferdate:
haveLoan:2
LoanName:
WeiFaName:6
FullAmountName:8
RunAreaCodeName:11
assignDriver:2
prpcinsureds[0].insuredname:
prpcinsureds[0].mobile:
prpcinsureds[0].email:
prpcinsureds[2].insuredname:在在在
prpcinsureds[2].identifytype:01
prpcinsureds[2].identifynumber:410421198902050047
insuredIdentifyAddr:在在在在在在在在 在
prpcinsureds[2].sex:2
prpcinsureds[2].age:27
prpcinsureds[2].mobile:13633485648
prpcinsureds[2].email:56465464@qq.com
isJZFullAmount:
WithdrawItemKindNo:
GlassTypeModel:
RadiusTypeModel:
ConcertedRateModel:
DeductibleSWITCH:
PersonTypeModel:
AccidentTypeModel:
NoCalculateFlag:
DemandNo:
DemandNoBI:
SAFE_ADJUST:
NONCLAIM_ADJUST:
LOYALTY_ADJUST:
RISK_FLAG:
blackforSY:0
ANameAreaCode:
CarClauseChgDate:
AddSubKindCode:
KindProfitFlag:
R_MAX_UNITAMOUNT:
B2Flag:B2C
sumAmount:0
tableShortRate_Flag:
Currency:CNY
CurrencyName:人民币
ShortRateFlag:2
ShortRate:100.0000
prpcmain.businessnature:5
AgentCode:
AgentName:
ThisDamagedCI:0
LastDamagedA:0
LastDamagedB:0
ThisDamagedA:0
ThisDamagedB:0
InsurerCode:0
AgentCodeSub:
claim_Amount:
LastPolicyNo:
AProfitRate:
BProfitRate:
DProfitRate:
ZProfitRate:
RenewalCIFlag:
RenewalBIFlag:
QueryNoCheck_CI:
QueryNoCheck_BI:
AnswerCI:
AnswerBI:
QueryCheckFlag:
QueryCheckFlagBI:
QuestionCI:
QuestionBI:
proposalNoUwderNoSY:
proposalNoUwderNoBZ:
CIrealkey:
CIdatakey:
BIrealkey:
BIdatakey:
OptionalPackageElements:
vehicle_style_opt:K33
isRecord:0
EconomyPackageDetail:
BasicPackageDetail:
ComprehensivePackageDetail:
OptionalPackageDetail:
car_sequence_no:
carShipTax.taxabatereason:
carShipTax.taxabatetype:
carShipTax.taxabateamount:
carShipTax.taxpayernumber:
carShipTax.dutypaidproofno:
carShipTax.taxexplanation:
carShipTax.taxtype:
TAX_FLAG:
PAY_NO:
DEPARTMENT:
proposalnoBI:
proposalnoCI:
New_VehicleFlag:
BZ_selected:0
isBusiness:
BZPremium:
bzEnable:1
dateSeprateConf:0
changeItemKind:
remindFlag:0
bz_changeFlag:1
shanxiHighPriRem:0
HBNoFullAmount:0
prpcitemCar.AkeyRenewalGuoHu:0
isFirst2201:0
firstToCaculate:0
isNeedCompare:0
isNeedCal:0
bonusAmount:
bonusEndDate:
CarKindCI:K33
TraveltaxAddress:10100
TraveltaxType:1
ChangeNationDate:
oldLicenseNo:
FTaxFlag:0
CarOwnerIdentifyType_BJ:01
CarOwnerIdentifyNumber_BJ:
BJFUEL_TYPE:
CERTIFICATE_TYPE:
CERTIFICATE_NO:
CERTIFICATE_DATE:
prpcitemCar.certificatedate:
startDateCI:
starthourCI:0
endDateCI:
endhourCI:24
carShipTax.taxpayername:
carShipTax.taxpayertype:01
carShipTax.taxpayeridentno:
CarIdentifyAddressSX:
CarNameSX:
CarKindSX:
PAY_NO_SH:
DEPARTMENT_SH:
TAX_FLAG_SH:N
buytax:on
insuredCount:1
othersNumber:2
othersCount:1
sendEmail:
callback_Phone:
callback_Name:\
'''

#第一次验证
postdata='''\
eadinsuredInfoTrandata:
eadinsuredInfoZ:
eadinsuredInfoTrandataZ:
zIsOnlyInsure:
zcopies:
zcountInsred:
eadThreeStepFlagZ:
carOwnerRemind:
majorFactoryFm:
lastCiEndDate:
hzPolicy:
cooperator:
tbOrderNo:
cooperatorFlag:false
telContact:1
onlineService:1
appCallback:1
wangyiCon:1
faq:1
reinsurance:
sendPrice:1
savePrice:1
carPeopleAccident:1
VIPFlag:
prpemployeeUserid:
pin:
pazxData:
haocheData:
mobilePhone:
provinceCode:
prpcmain.areaCode:41000000
prpcmain.areaCodeLast:41000000
prpcmain.cityCode:41010000
prpcmain.cityCodeLast:41010000
prpcitemCar.licenseno:008558
newCarEnableFlag_stepone:1
oldPolicyNo:
entryId:
ccaEntryId:
prpcmain.comcode:41010088
prpcmain.makecom:41010088
prpcmain.handlercode:4101880120
prpcmain.handler1code:4101880120
prpcmain.handler1code_uni:1241010107
prpcmain.handlercode_uni:1241010107
prpcmain.operatorcode:4101880120
branchcode:41010000
cityName:郑州
provinceName:河南
threeZuheFlag:0
threeZuhe:0
checkBZDate:
isrenewalonlycar:1
checkcode:
lastcarownername:
comcname:郑州
priceConfigKind:2
prpcmain.uniqueID:016dd87e-2360-4565-9905-082bf183cb18
deliverAddressFlag:1
serverDateTime:2016/3/2 10:02
userPriceConf:1
BM_flag:0
countyName:
oldinterimno:
TZFlag:
isblackFlag:
ccaEntryLinks:
ccaID:
ccaFlag:
toPageProposalZJson:
ccaemail:
itemKindFlag:caculateInfo
zancunmail:0
baojiaflag:0
taxEnable:1
BISigle:1
BZSigle:1
zSameAsFlag:000
quotepriceFlag:
phoneVerificationflag:0
driveAreaName:河南省内行驶
tokenNo:
frameNoBJ:
engineNoBJ:
carOwnerBJ:
renewalRand:
quickPrice:
prpcmain.renewal:2
agentTypeValue:
pos:
carInfoPos:
carInfoFromMyins:
CarModelType:
prpcitemCar.modelcode:DZABJD0007
prpcitemCar.purchaseprice:176900
isOutRenewal:0
lastHas050200:0
lastHas050500:0
lastHas050210:0
lastHas050310:0
lastHas050291:0
mrPurchasePrice:
oriPurchasePrice:
purchasePriceMin:
purchasePriceMax:
DQAmountMin:
DQAmountMax:
DQAmount:
purchasePriceByDeclinature:
nbCheckFlag:
prpcitemCar.countrynature:03
prpcitemCar.useyears:0
newCarMonths:12
prpcitemCar.licenseflag:0
prpcitemCar.newCar_check:on
prpcitemCar.newcarflag:0
prpcitemCar.carloanflag:0
prpcitemCar.transfervehicleflag:0
prpcitemCar.nonlocalflag:0
marketYear:
TonCount:
isHBpriceconfig:0
returnCarModelJson:
returnCarModelJsonTemp:
returnRenewalJson:
returnERiskJson:
beforeProposalNo:
renewalPackage:renewalPackage
hasRealTime:0
seatCountOri:5
queryPostCodeCity:
prpcinsureds[1].insurednature:3
prpcinsureds[1].:1
prpcinsureds[0].insuredflag:0010000
prpcinsureds[1].insuredflag:1000000
prpcinsureds[2].insuredflag:0100000
prpcinsureds[0].postcode:
prpcinsureds[0].insuredaddress:
renewalAppMobile:
BZ_timeChangeFlag:0
BI_timeChangeFlag:0
EnrollDateyc:1
returnNonRenewal:
tn_identityId:
cmpid:
carOwnerChangeFlag:0
prpcmain.changeFlag_renewal:0
packageFromQuick:
cooperatorFlag:false
prpcmain.packageName:EconomyPackage
prePackageName:
isNeedQueryCarModel:0
carInfoChangeFlag:1
StartDateJQ_renewal:
StartHourJQ_renewal:
guohutishi:0
nodamyearsBi:
purchasePrice_renewal:0
jyFlag:
jyType:
jyIcon:
jyBrandId:
jyFamilyId:
jyGroupId:
jyParentId:
jyParentName:
jyGearboxType:
jyImportFlag:1
showSeatCountFlag:
jyGroupPicData:/home/ecar/jy/pics/group/DZA2AH01/small/small_DZA2AH01_1.jpg,/home/ecar/jy/pics/group/DZA2AH01/small/small_DZA2AH01_2.jpg,/home/ecar/jy/pics/group/DZA2AH01/small/small_DZA2AH01_3.jpg
jyBrandPicData:
prpcitemCar.runmiles:10000
prpcitemCarext.nodamyearsbi:0
prpcmain.xzlastdamagedbi:0
oldframeno:
oldengineno:
prpcitemCar.frameno:LGXC16AF5G0008558
isFocus:0
prpcitemCar.vinno:LGXC16AF5G0008558
prpcitemCar.engineno:216005190
prpcitemCar.enrolldate:2016/03/02
prpcitemCar.brandname:大众汽车SVW71816EU
jyBrandName:
jyGroupName:请选择
jyDisplacement:请选择
jyGearboxName:请选择
jyParentVehName:请选择
jyFgwCode:请选择
prpcitemCar.aliasname:
prpcitemCar.seatcount:5
prpcmain.startdate:2016/03/03
prpcmain.starthour:0
prpcmain.enddate:2017/03/02
prpcmain.endhour:24
startDateBI:2016/03/03
starthourBI:0
endDateBI:2017/03/02
endhourBI:24
StartDateBIpro:24
endDateBIpro:24
startDateisChanged:0
prpcitemCar.TravelMilesvalue:1
guohuselect:0
prpcitemCar.transferdate:
haveLoan:2
LoanName:
WeiFaName:6
FullAmountName:8
RunAreaCodeName:11
assignDriver:2
prpcinsureds[0].insuredname:
prpcinsureds[0].mobile:
prpcinsureds[0].email:
prpcinsureds[2].insuredname:在在在
prpcinsureds[2].identifytype:01
prpcinsureds[2].identifynumber:410421198902050047
insuredIdentifyAddr:在在在在在在在在 在
prpcinsureds[2].sex:2
prpcinsureds[2].age:27
prpcinsureds[2].mobile:13633485648
prpcinsureds[2].email:56465464@qq.com
isJZFullAmount:
WithdrawItemKindNo:
GlassTypeModel:
RadiusTypeModel:
ConcertedRateModel:
DeductibleSWITCH:
PersonTypeModel:
AccidentTypeModel:
NoCalculateFlag:
DemandNo:
DemandNoBI:
SAFE_ADJUST:
NONCLAIM_ADJUST:
LOYALTY_ADJUST:
RISK_FLAG:
blackforSY:0
ANameAreaCode:
CarClauseChgDate:
AddSubKindCode:
KindProfitFlag:
R_MAX_UNITAMOUNT:
B2Flag:B2C
sumAmount:0
tableShortRate_Flag:
Currency:CNY
CurrencyName:人民币
ShortRateFlag:2
ShortRate:100.0000
prpcmain.businessnature:5
AgentCode:
AgentName:
ThisDamagedCI:0
LastDamagedA:0
LastDamagedB:0
ThisDamagedA:0
ThisDamagedB:0
InsurerCode:0
AgentCodeSub:
claim_Amount:
LastPolicyNo:
AProfitRate:
BProfitRate:
DProfitRate:
ZProfitRate:
RenewalCIFlag:
RenewalBIFlag:
QueryNoCheck_CI:
QueryNoCheck_BI:
AnswerCI:
AnswerBI:
QueryCheckFlag:
QueryCheckFlagBI:
QuestionCI:
QuestionBI:
proposalNoUwderNoSY:
proposalNoUwderNoBZ:
CIrealkey:
CIdatakey:
BIrealkey:
BIdatakey:
OptionalPackageElements:
vehicle_style_opt:K33
isRecord:0
EconomyPackageDetail:
BasicPackageDetail:
ComprehensivePackageDetail:
OptionalPackageDetail:
car_sequence_no:
carShipTax.taxabatereason:
carShipTax.taxabatetype:
carShipTax.taxabateamount:
carShipTax.taxpayernumber:
carShipTax.dutypaidproofno:
carShipTax.taxexplanation:
carShipTax.taxtype:
TAX_FLAG:
PAY_NO:
DEPARTMENT:
proposalnoBI:
proposalnoCI:
New_VehicleFlag:
BZ_selected:0
isBusiness:
BZPremium:
bzEnable:1
dateSeprateConf:0
changeItemKind:
remindFlag:0
bz_changeFlag:1
shanxiHighPriRem:0
HBNoFullAmount:0
prpcitemCar.AkeyRenewalGuoHu:0
isFirst2201:0
firstToCaculate:0
isNeedCompare:0
isNeedCal:0
bonusAmount:
bonusEndDate:
CarKindCI:K33
TraveltaxAddress:10100
TraveltaxType:1
ChangeNationDate:
oldLicenseNo:
FTaxFlag:0
CarOwnerIdentifyType_BJ:01
CarOwnerIdentifyNumber_BJ:
BJFUEL_TYPE:
CERTIFICATE_TYPE:
CERTIFICATE_NO:
CERTIFICATE_DATE:
prpcitemCar.certificatedate:
startDateCI:
starthourCI:0
endDateCI:
endhourCI:24
carShipTax.taxpayername:
carShipTax.taxpayertype:01
carShipTax.taxpayeridentno:
CarIdentifyAddressSX:
CarNameSX:
CarKindSX:
PAY_NO_SH:
DEPARTMENT_SH:
TAX_FLAG_SH:N
buytax:on
insuredCount:1
othersNumber:2
othersCount:1
sendEmail:
callback_Phone:
callback_Name:\
'''

yanzheng='http://www.epicc.com.cn/ecar/underwrite/underwrite/underwriteCheckProfit?time=1456561838870'
#prpcmainuniqueID='016dd87e-2360-4565-9905-082bf183cb18'
postdata=postdata.replace('[prpcmain.uniqueID]',prpcmainuniqueID)
r=http.posturl(yanzheng,postdata)
if not http.lasterror:
    content=r.read().decode()
    jso=json.loads(content)
    if jso[1]=='3':
        print(jso)
    else:
        print('error')
    print(jso)

postdata='''\
cooperatorFlag:false
telContact:1
onlineService:1
appCallback:1
wangyiCon:1
faq:1
sendPrice:1
savePrice:1
carPeopleAccident:1
prpcmain.areaCode:41000000
prpcmain.areaCodeLast:41000000
prpcmain.cityCode:41010000
prpcmain.cityCodeLast:41010000
prpcitemCar.licenseno:008558
newCarEnableFlag_stepone:1
prpcmain.comcode:41010088
prpcmain.makecom:41010088
prpcmain.handlercode:4101880120
prpcmain.handler1code:4101880120
prpcmain.handler1code_uni:1241010107
prpcmain.handlercode_uni:1241010107
prpcmain.operatorcode:4101880120
branchcode:41010000
cityName:郑州
provinceName:河南
threeZuheFlag:0
threeZuhe:0
isrenewalonlycar:1
comcname:郑州
priceConfigKind:2
prpcmain.uniqueID:[prpcmain.uniqueID]
deliverAddressFlag:1
serverDateTime:2016/2/27 14:36
userPriceConf:1
BM_flag:0
itemKindFlag:caculateInfo
zancunmail:0
baojiaflag:0
taxEnable:1
BISigle:1
BZSigle:1
zSameAsFlag:000
phoneVerificationflag:0
driveAreaName:河南省内行驶
prpcmain.renewal:2
prpcitemCar.modelcode:BJGAED0001
prpcitemCar.purchaseprice:76800
isOutRenewal:0
lastHas050200:0
lastHas050500:0
lastHas050210:0
lastHas050310:0
lastHas050291:0
mrPurchasePrice:76800
oriPurchasePrice:83400
purchasePriceMin:53760
purchasePriceMax:99840
prpcitemCar.countrynature:01
prpcitemCar.useyears:0
newCarMonths:12
prpcitemCar.licenseflag:0
prpcitemCar.newCar_check:on
prpcitemCar.newcarflag:0
prpcitemCar.carloanflag:0
prpcitemCar.transfervehicleflag:0
prpcitemCar.nonlocalflag:0
isHBpriceconfig:0
renewalPackage:renewalPackage
hasRealTime:0
seatCountOri:5
prpcinsureds[1].insurednature:3
prpcinsureds[1].:1
prpcinsureds[0].insuredflag:0010000
prpcinsureds[1].insuredflag:1000000
prpcinsureds[2].insuredflag:0100000
BZ_timeChangeFlag:0
BI_timeChangeFlag:0
EnrollDateyc:1
carOwnerChangeFlag:0
prpcmain.changeFlag_renewal:0
cooperatorFlag:false
prpcmain.packageName:EconomyPackage
isNeedQueryCarModel:0
carInfoChangeFlag:1
guohutishi:0
purchasePrice_renewal:0
jyIcon:B
jyImportFlag:0
brand/BJA8.jpg|北汽幻速
prpcitemCar.runmiles:10000
prpcitemCarext.nodamyearsbi:0
prpcmain.xzlastdamagedbi:0
prpcitemCar.frameno:LGXC16AF5G0008558
isFocus:0
prpcitemCar.vinno:LGXC16AF5G0008558
prpcitemCar.engineno:216005190
prpcitemCar.enrolldate:2016/02/27
prpcitemCar.brandname:宝骏LZW6465UVF
jyGroupName:请选择
jyDisplacement:请选择
jyGearboxName:请选择
jyParentVehName:请选择
jyFgwCode:请选择
prpcitemCar.seatcount:5
prpcmain.startdate:2016/02/28
prpcmain.starthour:0
prpcmain.enddate:2017/02/27
prpcmain.endhour:24
startDateBI:2016/02/28
starthourBI:0
endDateBI:2017/02/27
endhourBI:24
StartDateBIpro:24
endDateBIpro:24
startDateisChanged:0
prpcitemCar.TravelMilesvalue:1
guohuselect:0
haveLoan:2
WeiFaName:6
FullAmountName:8
RunAreaCodeName:11
assignDriver:2
prpcinsureds[2].insuredname:李若雯
prpcinsureds[2].identifytype:01
prpcinsureds[2].identifynumber:410421198902050047
insuredIdentifyAddr:加国中加国另另另中
prpcinsureds[2].sex:2
prpcinsureds[2].age:27
prpcinsureds[2].mobile:13598745896
prpcinsureds[2].email:735585858@qq.com
blackforSY:0
B2Flag:B2C
sumAmount:0
Currency:CNY
CurrencyName:人民币
ShortRateFlag:2
ShortRate:100.0000
prpcmain.businessnature:5
ThisDamagedCI:0
LastDamagedA:0
LastDamagedB:0
ThisDamagedA:0
ThisDamagedB:0
InsurerCode:0
vehicle_style_opt:K33
isRecord:0
BZ_selected:0
bzEnable:1
dateSeprateConf:0
remindFlag:0
bz_changeFlag:1
shanxiHighPriRem:0
HBNoFullAmount:0
prpcitemCar.AkeyRenewalGuoHu:0
isFirst2201:0
firstToCaculate:0
isNeedCompare:0
isNeedCal:0
CarKindCI:K33
TraveltaxAddress:10100
TraveltaxType:1
FTaxFlag:0
CarOwnerIdentifyType_BJ:01
starthourCI:0
endhourCI:24
carShipTax.taxpayertype:01
TAX_FLAG_SH:N
buytax:on
insuredCount:1
othersNumber:2
othersCount:1\
'''
#prpcmainuniqueID='0de6c1e4-1c03-445d-9c47-0e6586915eed'

#prpcmainuniqueID='4d352e8b-9c25-40b3-a1fe-8e7fd68336e4'
postdata=postdata.replace('[prpcmain.uniqueID]',prpcmainuniqueID)
url='http://www.epicc.com.cn/ecar/caculate/caculateForBatch?time=1456540973665'
r=http.posturl(url,postdata)
if not http.lasterror:
    content=r.read().decode()
    jso=json.loads(content)
    if jso['errorMsg']=='成功':
        pricelist=jso['CommonPackage']
        print(pricelist)
    else:
        print('error')
    print(jso)
#os.system('pause')