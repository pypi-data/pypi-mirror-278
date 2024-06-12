from collections import Counter
import email
import email.message

class EmailInsights:

    def __init__(self):
        pass

    def _get_email_structure(self, email_text):
        """
        Shows the structure of the email object.

        Parameters
        ----------
            email_text : email.message.EmailMessage
                the email object in consideration.
        """
        if email_text is None:
            raise Exception(f"Input can not be {None}")
        else:
            if isinstance(email_text, str):
                return email_text
            payload = email_text.get_payload()
            if isinstance(payload, list):
                multipart = ", ".join([self._get_email_structure(sub_email) for sub_email in payload])
                return f"multipart({multipart})"
            else:
                return email_text.get_content_type()

    def count_email_structures(self, emails):
        """
        Shows the structures of an email object(s) with their corresponding frequencies in descending order.

        Parameters
        ----------
            emails : list or tuple or email.message.Message
                the collection of email objects to be considered.
        """
        if isinstance(emails, (list, tuple)):
            structures = Counter()
            for email_ in emails:
                structure = self._get_email_structure(email_)
                structures[structure] += 1
            return structures.most_common()
        elif isinstance(emails, email.message.Message):
                return self._get_email_structure(emails)
        else:    
            print(f"Input must be type list or tuple or email.message.Message not {type(emails)}")
