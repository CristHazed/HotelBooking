from .exceptions import InvalidContactError, InvalidGuestNameError

class Guest:
    def __init__(self, name, email="", phone=""):
        self.name = name
        self.email = email
        self.phone = (phone or "").strip()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        value = " ".join(str(value or "").split())
        if not value:
            raise InvalidGuestNameError("Please enter a valid guest name.")
        if len(value) < 2:
            raise InvalidGuestNameError("Guest name must be at least 2 letters.")
        for letter in value:
            if not (letter.isalpha() or letter in " .'-"):
                raise InvalidGuestNameError(
                    "Guest name can only have letters, spaces, apostrophes, hyphens and periods."
                )
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        value = (value or "").strip()
        if value and ("@" not in value or "." not in value.split("@")[-1]):
            raise InvalidContactError("Please enter a valid email, like name@example.com.")
        self._email = value

    def to_dict(self):
        return {"name": self._name, "email": self._email, "phone": self.phone}

    def __str__(self):
        return self._name