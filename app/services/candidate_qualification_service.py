from dataclasses import dataclass

from app.core.candidate_status import CandidateQualificationStatus
from app.core.text_normalization import normalize_for_keyword_match


@dataclass(frozen=True)
class QualificationDecision:
    qualification_status: str
    reason: str


class CandidateQualificationService:
    REJECT_KEYWORDS = {
        "anti radar": "produto voltado a burlar fiscalizacao",
        "6mm": "item associado a arma/airsoft",
        "airsoft": "item regulado ou sensivel",
        "pcp": "item associado a arma de pressao",
        "rossi": "termo associado a arma/airsoft",
        "beeman": "termo associado a arma de pressao",
        "municao": "item regulado",
        "arma": "item regulado",
        "revolver": "item regulado",
    }

    REVIEW_KEYWORDS = {
        "iphone": "marca forte; revisar concorrencia e margem",
        "xiaomi": "marca forte; revisar concorrencia e margem",
        "ps4": "item com concorrencia possivelmente alta",
        "tablet": "termo generico; revisar especificidade",
        "celular": "termo generico; revisar especificidade",
    }

    def qualify(self, term: str) -> QualificationDecision:
        normalized = normalize_for_keyword_match(term)

        for keyword, reason in self.REJECT_KEYWORDS.items():
            if keyword in normalized:
                return QualificationDecision(
                    qualification_status=CandidateQualificationStatus.REJECTED,
                    reason=reason,
                )

        for keyword, reason in self.REVIEW_KEYWORDS.items():
            if keyword in normalized:
                return QualificationDecision(
                    qualification_status=CandidateQualificationStatus.NEEDS_REVIEW,
                    reason=reason,
                )

        return QualificationDecision(
            qualification_status=CandidateQualificationStatus.APPROVED,
            reason="candidato elegivel para enriquecimento inicial",
        )
