from .settings import settings
from .str2dict import str2dict
from zxcvbn import zxcvbn
from password_strength import PasswordPolicy, PasswordStats



class PasswordStrengthError(Exception):
    pass

def check_password(password: str):

    if settings.password_zxcvbn is not None:
        zr = zxcvbn(password)
        print("ZXCVB", zr)
        score = zr['score']
        feedback = zr['feedback']
        if score < settings.password_zxcvbn:
            msg = ""
            if feedback['warning']:
                msg += feedback['warning'] + "\n"
            if feedback['suggestions']:
                msg += "\n".join(feedback['suggestions']) + "\n"
            raise PasswordStrengthError("Password too weak. " + msg)

    if settings.password_strength_policy is not None:
        d = str2dict(settings.password_strength_policy, 
                     fields={'length': int, 'uppercase': int, 'numbers': int, 'special': int, 
                             'nonletters': int, 'entropybits': int, 'strength': float})
        policy = PasswordPolicy.from_names(**d)
        
        tested_password = policy.password(password)

        msg=""

        for x in tested_password.test():
            print(x)
            msg += f"Must have {x.args[0]} {x.name()}. "
        
        if policy.test(password):
            raise PasswordStrengthError(msg)
