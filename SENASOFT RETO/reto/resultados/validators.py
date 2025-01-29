# usuarios/validators.py
import dns.resolver
from django.core.exceptions import ValidationError

def validate_email_domain(value):
    """
    Valida una dirección de correo electrónico comprobando si el dominio tiene registros MX.
    """
    try:
        domain = value.split('@')[1]
        dns.resolver.resolve(domain, 'MX')
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        raise ValidationError("El dominio del correo electrónico no tiene registros MX válidos.")
    except Exception as e:
        raise ValidationError(f"Error al validar el correo electrónico: {e}")
