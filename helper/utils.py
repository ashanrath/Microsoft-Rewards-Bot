def hide_email(email: str):
    email_parts = email.split('@')
    return f'{email_parts[0][:2]}{"*"*(len(email_parts[0])-3)}{email_parts[0][-1]}@{email_parts[1]}'