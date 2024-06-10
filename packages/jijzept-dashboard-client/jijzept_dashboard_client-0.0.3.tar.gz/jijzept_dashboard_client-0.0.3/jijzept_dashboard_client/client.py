import os
import typing as tp
from http import HTTPStatus

import requests

from jijzept_dashboard_client.exception import JijZeptDashboardClientError
from jijzept_dashboard_client.problem import Problem


class JijZeptDashboardClientConfig:
    def __init__(
        self,
        url: tp.Optional[str] = None,
        email: tp.Optional[str] = None,
        password: tp.Optional[str] = None,
    ) -> None:
        if url is None:
            try:
                url = os.environ["JIJZEPT_DASHBOARD_URL"]
            except KeyError as e:
                raise JijZeptDashboardClientError(
                    "Please set either the argument `url` or "
                    "the environment variable `JIJZEPT_DASHBOARD_URL`."
                ) from e

        if email is None:
            try:
                email = os.environ["JIJZEPT_DASHBOARD_EMAIL"]
            except KeyError as e:
                raise JijZeptDashboardClientError(
                    "Please set either the argument `email` or "
                    "the environment variable `JIJZEPT_DASHBOARD_EMAIL`."
                ) from e

        if password is None:
            try:
                password = os.environ["JIJZEPT_DASHBOARD_PASSWORD"]
            except KeyError as e:
                raise JijZeptDashboardClientError(
                    "Please set either the argument `password` or "
                    "the environment variable `JIJZEPT_DASHBOARD_PASSWORD`."
                ) from e

        self._url = url
        self._email = email
        self._password = password

    @property
    def url(self) -> str:
        return self._url

    @property
    def email(self) -> str:
        return self._email

    @property
    def password(self) -> str:
        return self._password


class JijZeptDashboardClient:
    _config: tp.Optional[JijZeptDashboardClientConfig] = None
    _header: tp.ClassVar[dict[str, str]] = {"Content-Type": "application/json"}

    def __init__(
        self,
        url: tp.Optional[str] = None,
        email: tp.Optional[str] = None,
        password: tp.Optional[str] = None,
    ) -> None:
        """
        Initialize the JijZept Dashboard Client.

        You can use the `JIJZEPT_DASHBOARD_URL` environment variable
        instead of `url`, the `JIJZEPT_DASHBOARD_EMAIL` environment
        variable instead of `email`, and the `JIJZEPT_DASHBOARD_PASSWORD`
        environment variable instead of `password`.

        Args:
            url (str, optional): The base URL of the JijZept Dashboard API.
            email (str, optional): The email address for authentication.
            password (str, optional): The password for authentication.

        Raises:
            JijZeptDashboardClientError: If some settings are missing

        Examples:
            A example of setting the configuration with the arguments:

            ```python
            import jijzept_dashboard_client as jdc
            client = jdc.JijZeptDashboardClient(
                url="https://jijzept-dashboard.example.com",
                email="test@example.com",
                password="password",
            )
            ```

        """
        self._config = JijZeptDashboardClientConfig(
            url=url, email=email, password=password
        )

    def request_auth(self) -> str:
        """
        Request authentication to the JijZept Dashboard.

        Returns:
            str: The access token for the JijZept Dashboard.
        """
        if self._config is None:
            raise JijZeptDashboardClientError("The configuration is not set.")

        url = self._config.url
        email = self._config.email
        password = self._config.password

        response = requests.post(
            url=url + "/token",
            data={"username": email, "password": password},
        )

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise JijZeptDashboardClientError(
                "Failed to authenticate with the JijZept Dashboard API. "
                "Please check the `email` and `password`."
            ) from e

        try:
            token = response.json()["access_token"]
        except KeyError as e:
            raise JijZeptDashboardClientError(
                "Failed to get the token from the JijZept Dashboard API. "
                "Please update `jijzept_dashboard_client` or check the `url`."
            ) from e

        self._header["Authorization"] = f"Bearer {token}"

        return token

    def register_model(
        self,
        problem: Problem,
        project_id: int,
    ) -> requests.Response:
        """
        Register the mathematical model to the JijZept Dashboard.

        Args:
            problem (Problem): The problem to register.
            project_id (int): ID of the project to which you are registering.

        Returns:
            requests.Response: The response from the JijZept Dashboard.

        Raises:
            JijZeptDashboardClientError: If the configuration is not set.

        Examples:
            ```python
            import jijmodeling as jm
            import jijzept_dashboard_client as jdc

            # Define placeholder, element, decision variables
            d = jm.Placeholder("d", ndim=2, description="Distance matrix")
            N = d.len_at(0, latex="N", description="Number of cities")
            i = jm.Element("i", belong_to=(0, N), description="City index")
            j = jm.Element("j", belong_to=(0, N), description="City index")
            t = jm.Element("t", belong_to=(0, N), description="City index")
            x = jm.BinaryVar(
                "x", shape=(N, N), description="Assignment matrix"
            )

            # Define the problem with descriptions
            problem = jdc.Problem("TSP")
            problem += (
                jm.sum(
                    [i, j], d[i, j] * jm.sum(t, x[i, t] * x[j, (t + 1) % N])
                ),
                "Minimize total distance",
            )
            problem += (
                jm.Constraint("one-city", jm.sum(i, x[i, t]) == 1, forall=t),
                "Each city is visited exactly once",
            )
            problem += (
                jm.Constraint("one-time", jm.sum(t, x[i, t]) == 1, forall=i),
                "Each person visits exactly one city",
            )

            # Initialize JijZeptDashboardClient
            client = jdc.JijZeptDashboardClient(
                url="http://0.0.0.0:8080",
                email="tester@j-ij.com",
                password="test#password",
            )
            # Register the mathematical model
            response = client.register_model(problem, 1)
            ```

        """
        if self._config is None:
            raise JijZeptDashboardClientError("The configuration is not set.")

        # Request authentication if the token is not set
        if "Authorization" not in self._header:
            self.request_auth()

        request_url = (
            self._config.url + f"/project/{project_id!s}/mathematical_model/"
        )

        response = requests.post(
            url=request_url,
            headers=self._header,
            json=problem.to_serializable(),
        )

        if response.status_code == HTTPStatus.OK:
            print(
                "[SUCCESS] The mathematical model was successfully registered."
            )
        else:
            print("[FAILED] Failed to register the mathematical model.")

        return response
