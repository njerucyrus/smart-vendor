class PhoneNumberUtils:
    @classmethod
    def clean(cls, phone_number):
        phone = list(phone_number)
        prefix = phone[0]
        length = len(phone_number)

        if prefix == '0' and length == 10:
            phone[0] = '254'
            return "".join(phone)

        elif prefix == '2' and length == 12:
            return str(phone_number)

        elif length == 9:
            return f'254{phone_number}'

        else:
            return ''

if __name__ == '__main__':
    clean_phone = PhoneNumberUtils.clean("0703191981")
    print(clean_phone)