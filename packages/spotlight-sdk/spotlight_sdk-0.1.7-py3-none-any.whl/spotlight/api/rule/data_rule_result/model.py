from spotlight.core.common.base import Base


class DataRuleResultResponse(Base):
    id: str
    data_rule_id: str
    record_id: str
    timestamp: int
