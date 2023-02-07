from functools import cached_property

from translators import (
    ListTranslator,
    ThreatTranslator,
    StatisticsThreatsTranslator
)
from services import ConfigService
from repositories import ThreatsRepository
from wrappers import (
    MatplotlibWrapper,
    TelethonWrapper
)
from telegram_scraper import TelegramScraper
from constants import (
    KEYWORD_DATABASE_IDENTIFIERS_PAIRS,
    KEYWORD_THREAT_TYPE_PAIRS,
    FIELD_TYPE,
    FIELD_DATABASE_IDENTIFIERS
)
from parsers import (
    CWEParser,
    CVEParser,
    BduFSTECParser,
    SignParser
)


class Structure:
    @cached_property
    def telegram_api_id(self):
        return self.config_service.telegram_api_id

    @cached_property
    def telegram_api_hash(self):
        return self.config_service.telegram_api_hash

    @cached_property
    def telegram_phone(self):
        return self.config_service.telegram_phone

    @cached_property
    def telegram_client(self):
        return TelethonWrapper(
            self.telegram_phone,
            self.telegram_api_id,
            self.telegram_api_hash
        ).get_client()

    @cached_property
    def telegram_scraper(self):
        return TelegramScraper(
            self.telegram_client,
            self.database_identifiers_parser,
            self.threat_type_parser
        )

    @cached_property
    def database_identifiers_parser(self):
        return SignParser(
            KEYWORD_DATABASE_IDENTIFIERS_PAIRS,
            FIELD_DATABASE_IDENTIFIERS,
            [
                self.bdu_fsctec_parser,
                self.cve_parser,
                self.cwe_parser
            ]
        )

    @cached_property
    def threat_type_parser(self):
        return SignParser(
            KEYWORD_THREAT_TYPE_PAIRS,
            FIELD_TYPE,
            [
                self.bdu_fsctec_parser,
                self.cve_parser,
                self.cwe_parser
            ]
        )

    @cached_property
    def config_service(self):
        return ConfigService()

    @cached_property
    def threat_translator(self):
        return ThreatTranslator()

    @cached_property
    def threats_translator(self):
        return ListTranslator(self.threat_translator)

    @cached_property
    def statistics_threats_translator(self):
        return StatisticsThreatsTranslator()

    @cached_property
    def threats_repository(self):
        return ThreatsRepository(
            self.threats_translator,
            self.statistics_threats_translator
        )

    @cached_property
    def matplotlib_wrapper(self):
        return MatplotlibWrapper()

    @cached_property
    def cve_parser(self):
        return CVEParser()

    @cached_property
    def cwe_parser(self):
        return CWEParser()

    @cached_property
    def bdu_fsctec_parser(self):
        return BduFSTECParser()


structure = Structure()
