from email_validator import validate_email, EmailNotValidError
import os;


def string_length_validator(string: str, length: int = 255):
  if len(string) > length:
    return False;
  return True;

def email_validator(email: str) -> str | bool:
  try:
    is_email_valid = validate_email(email);

    return is_email_valid.normalized # retorna email normalizado
  except EmailNotValidError as err:
    return False
  
