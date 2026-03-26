from dataclasses import dataclass


@dataclass(frozen=True)
class QualificationDecision:
    qualification_status: str
    reason: str


class CandidateQualificationService:
    REJECT_KEYWORDS = {
        "anti radar": "produto voltado a burlar fiscalizaçao",
        "6mm": "item associado a arma/airsoft",
        "airsoft": "item regulado ou sensivel",
        "pcp": "item associado a arma de pressao",
        "rossi": "termo associado a arma/airsoft",
        "beeman": "termo associado a arma de pressao",
        "munição": "item regulado",
        "municao": "item regulado",
        "arma": "item regulado",
        "revólver": "item regulado",
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
        normalized = self._normalize(term)

        for keyword, reason in self.REJECT_KEYWORDS.items():
            if keyword in normalized:
                return QualificationDecision(
                    qualification_status="rejected",
                    reason=reason,
                )

        for keyword, reason in self.REVIEW_KEYWORDS.items():
            if keyword in normalized:
                return QualificationDecision(
                    qualification_status="needs_review",
                    reason=reason,
                )

        return QualificationDecision(
            qualification_status="approved",
            reason="candidato elegivel para enriquecimento inicial",
        )

    @staticmethod
    def _normalize(term: str) -> str:
        return " ".join(term.strip().lower().split())
