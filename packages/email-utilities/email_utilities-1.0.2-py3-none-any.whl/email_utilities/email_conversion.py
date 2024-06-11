import email.parser
import email.policy
import re
from html import unescape


class EmailConversion:
    """
      A class to convert email to text.

      ...

      Attributes
      ----------
      filepath : str or Path object
          the location of the email file to be considered.

      Methods
      -------
      load_email(file_location):
          Loads the email in consideration from file_location.
      """

    def __init__(self, filepath=None):
        self.filepath = filepath

    def load_email(self, file_location=None):
        """
        Loads the email file from the filepath argument.

        Parameters
        ----------
            file_location : str or Path object
                the location of the file to be loaded.
        """
        if self.filepath:
            file_location = self.filepath
        try:
            with open(file_location, "rb") as file:
                return email.parser.BytesParser(policy=email.policy.default).parse(file)
        except FileNotFoundError:
            print("The file can't be found")
        except TypeError:
            print(f"expected str, bytes or os.PathLike object, not {type(self.filepath)}")

    def _convert_html_to_plain_text(self, email_text=None):
        """
        Converts html-like email to text.

        Parameters
        ----------
            email_text : email.message.Message
                the email to be converted to text.
        """

        if self.filepath and email_text is None:
            email_text = self.load_email()
        if email_text.get_content_type() == "text/html":
            # noinspection PyBroadException
            try:
                email_text = email_text.get_content()
            except:  # in case of encoding issues
                email_text = str(email_text.get_payload())
            email_text = re.sub('<head.*?>.*?</head>', '', email_text, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)
            email_text = re.sub('<a\s.*?>', ' HYPERLINK ', email_text, flags=re.MULTILINE | re.DOTALL | re.I)
            email_text = re.sub('<.*?>', '', email_text, flags=re.MULTILINE | re.DOTALL)
            email_text = re.sub(r'(\s*\n)+', '\n', email_text, flags=re.MULTILINE | re.DOTALL)
            return unescape(email_text)
        else:
            print(f"The email is a {email_text.get_content_type()} type instead of html")

    def convert_email_to_text(self, email_text=None):
        """
        Converts email to text.

        Parameters
        ----------
            email_text : email.message.Message
                the email message object to be converted.
        """

        if self.filepath and email_text is None:
            email_text = self.load_email()
        for component in email_text.walk():
            content_type = component.get_content_type()
            if content_type not in ("text/plain", "text/html"):
                continue
            if content_type == "text/plain":
                return component
            else:
                return self._convert_html_to_plain_text(component)
