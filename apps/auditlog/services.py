from apps.auditlog.models import AuditLog


def record_audit_event(*, actor_user, action: str, target_model: str, target_id: str, detail: str = "", ip_address=None):
    return AuditLog.objects.create(
        actor_user=actor_user,
        action=action,
        target_model=target_model,
        target_id=str(target_id),
        detail=detail,
        ip_address=ip_address,
    )
