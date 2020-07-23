import unittest
from unittest import mock

from schema.user import UserSchema

from service.authentication import (
    JWT,
    JWTExceptionExpired,
    AuthenticationService,
    EmailOrPasswordInvalid
)


class AuthenticationServiceTest(unittest.TestCase):
    
    def test_authenticate_with_exception(self):
        # arrange
        session_mock = mock.MagicMock()
        session_mock\
            .query.return_value\
            .filter.return_value\
            .filter.return_value\
            .all.return_value = None

        # act / assert
        with self.assertRaises(EmailOrPasswordInvalid):
            AuthenticationService(session_mock)._authenticate(
                email='test@test', 
                password='test'
            )

    def test_authenticate_with_success(self):
        # arrange
        user = UserSchema(
            email='test@test',
            password='test'
        )

        session_mock = mock.MagicMock()
        session_mock\
            .query.return_value\
            .filter.return_value\
            .filter.return_value\
            .all.return_value = user

        # act
        result = AuthenticationService(session_mock)._authenticate(
            email='test@test', 
            password='test'
        )

        # assert
        self.assertTrue(result)


class JWTTest(unittest.TestCase):

    def test_validate_with_exception(self):
        # act / assert
        with self.assertRaises(JWTExceptionExpired):
            JWT().validate(
                'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.'\
                'eyJlbWFpbCI6ImZlZ2hpc2lAZ21haWwuY29tIiwiZXhwIjoxNTk1NTEwNTcwfQ.'\
                'O4_o7OTMdo5ZXnlti2a6br5ZImsafD5YXTZx-54yPWw'
            )

    def test_validate_with_success(self):
        # arrange
        token = JWT().get({
            'email': 'test@test'
        })

        # act
        result = JWT().validate(token)
        
        # assert
        self.assertEqual(result['email'], 'test@test')