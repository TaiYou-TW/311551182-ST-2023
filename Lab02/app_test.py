import unittest
from unittest.mock import patch, Mock, call
from app import *


class ApplicationTest(unittest.TestCase):
    people = ["William", "Oliver", "Henry", "Liam"]
    selected = ["William", "Oliver", "Henry"]
    random_list = ["William", "Oliver", "Henry", "Liam"]

    def fake_mailsystem_write(self, name):
        content = f"Congrats, {name}!"
        print(content)
        return content

    def setUp(self):
        with patch.object(Application, "__init__", return_value=None):
            app = Application()

            # Init property
            app.people = self.people
            app.selected = self.selected

            # Mock method with given sequential responses
            app.get_random_person = Mock()
            app.get_random_person.side_effect = self.random_list

            # Mock MailSystem
            mailSystem = MailSystem()

            mailSystem.send = Mock(return_value=None)
            mailSystem.send.side_effect = lambda name, content: None

            mailSystem.write = Mock(return_value=None)
            mailSystem.write.side_effect = self.fake_mailsystem_write

            app.mailSystem = mailSystem

            self.application = app

    def test_app(self):
        app = self.application

        # test `select_next_person()`
        first_person = app.select_next_person()
        print(f"1st time of `select_next_person`: {first_person} selected")
        self.assertEqual(first_person, self.people[3])

        second_person = app.select_next_person()
        print(f"2nd time of `select_next_person`: {second_person} selected")
        self.assertEqual(second_person, None)

        third_person = app.select_next_person()
        print(f"3rd time of `select_next_person`: {third_person} selected")
        self.assertEqual(third_person, None)

        fourth_person = app.select_next_person()
        print(f"4th time of `select_next_person`: {fourth_person} selected")
        self.assertEqual(fourth_person, None)

        # test MailSystem
        app.notify_selected()

        self.assertEqual(app.mailSystem.send.call_count, 4)
        self.assertEqual(app.mailSystem.write.call_count, 4)

        print(app.mailSystem.write.call_args_list)
        self.assertEqual(
            app.mailSystem.write.call_args_list,
            [
                call("William"),
                call("Oliver"),
                call("Henry"),
                call("Liam"),
            ],
        )
        print(app.mailSystem.send.call_args_list)
        self.assertEqual(
            app.mailSystem.send.call_args_list,
            [
                call("William", "Congrats, William!"),
                call("Oliver", "Congrats, Oliver!"),
                call("Henry", "Congrats, Henry!"),
                call("Liam", "Congrats, Liam!"),
            ],
        )


if __name__ == "__main__":
    unittest.main()