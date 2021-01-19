from dataclasses_serialization.json import JSONSerializer

from services.models.job import BridgeTxInfo, JobTxInfo

job = JobTxInfo('123', JobTxInfo.STATUS_ACTIVE, chain='BNB', intx_time=0,
                in_tx=BridgeTxInfo(
                    'BNB', 66312, 100.4, 'bnb123', '', '49394034930434093409343', 2302303
                ),
                out_tx=BridgeTxInfo(
                    'ETH', 5454343, 100.1, '', '0xC349309232ABC', '3432423292832983', 2302305
                ))


print(JSONSerializer.serialize(job))

j = JSONSerializer.serialize(job)
out_job = JSONSerializer.deserialize(JobTxInfo, j)
print(out_job)
assert job == out_job
