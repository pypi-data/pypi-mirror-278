import os
from pathlib import Path
from typing import Union
from urllib.parse import urlparse


from whiffle_client.decorators import load_data
from whiffle_client.io import download_write_chunks, VALID_DOWNLOAD_FILES
from whiffle_client.wind.mapping.base import BaseMapping
from whiffle_client.wind.components.wind_simulation_task import WindSimulationTask


class WindSimulationTaskEndpoints(BaseMapping):

    URL = "/api/v1/wind"
    RESOURCE_TYPE = "WindSimulationTask"

    @load_data(WindSimulationTask)
    def add(
        self,
        data: Union[str, dict, Path, WindSimulationTask] = None,
    ) -> WindSimulationTask:
        """Add new Wind Simulation Task

        Parameters
        ----------
        data : Union[str, dict, Path, WindSimulationTask], optional
            Either a path to a yaml, the data itself as a dictionary or a WindSimulationTask object
            containing the parameters that define the wind simulation task, by default None

        Returns
        -------
        WindSimulationTask
            Object instance of the wind simulation
        """
        wind_simulation_task = self.session.post_request(
            f"{self.session.server_url}{self.URL}", data=data
        )
        return WindSimulationTask.from_dict(wind_simulation_task.json())

    @load_data(WindSimulationTask)
    def edit(
        self,
        wind_simulation_task_id: str,
        data: Union[str, dict, Path, WindSimulationTask] = None,
    ) -> WindSimulationTask:
        """Edit existing Wind Simulation Task

        Parameters
        ----------
        wind_simulation_task_id : str
            Id of wind simulation task
        data : Union[str, dict, Path, WindSimulationTask], optional
            Either a path to a yaml, the data itself as a dictionary or a WindSimulationTask object
            containing the parameters that define the wind simulation task, by default None

        Returns
        -------
        WindSimulationTask
            Object instance of the wind simulation
        """
        request = self.session.put_request(
            f"{self.session.server_url}{self.URL}/{wind_simulation_task_id}",
            data=data,
        )
        return WindSimulationTask.from_dict(request.json())

    def submit(self, wind_simulation_task_id: str) -> WindSimulationTask:
        """Submit Wind Simulation Task

        Parameters
        ----------
        wind_simulation_task_id : str
            Id of wind simulation task

        Returns
        -------
        WindSimulationTask
            Object instance of the wind simulation
        """
        request = self.session.post_request(
            f"{self.session.server_url}{self.URL}/{wind_simulation_task_id}/submit",
        )
        return WindSimulationTask.from_dict(request.json())

    # Wind simulation commands
    def get_all(self) -> list[WindSimulationTask]:
        """Get a list of all the Wind Simulation Tasks available to the user

        Returns
        -------
        list[WindSimulationTask]
            List of WindSimulationTasks object instances
        """
        request = self.session.get_request(f"{self.session.server_url}{self.URL}")
        return [
            WindSimulationTask.from_dict(wind_simulation_tasks_params)
            for wind_simulation_tasks_params in request.json()
        ]

    def get(self, wind_simulation_task_id: str) -> WindSimulationTask:
        """Get a Wind Simulation Task

        Parameters
        ----------
        wind_simulation_task_id : str
            Id of wind simulation

        Returns
        -------
        WindSimulationTask
            Requested WindSimulationTask
        """
        return WindSimulationTask.from_dict(
            self.session.get_request(
                f"{self.session.server_url}{self.URL}/{wind_simulation_task_id}"
            ).json()
        )

    def delete(self, wind_simulation_task_id: str):
        """Delete Wind Simulation

        NOTE: Just Wind Simulation Tasks in 'drafted' status can be deleted

        Parameters
        ----------
        wind_simulation_task_id : str
            Id of wind simulation

        Returns
        -------
        dict
            Dictionary with the deleted WindSimulationTask id
        """
        return self.session.delete_request(
            f"{self.session.server_url}{self.URL}/{wind_simulation_task_id}"
        ).json()

    def download(
        self,
        wind_simulation_task_id: str,
        file: str = "results",
        output_name: str = None,
        output_dir: str = None,
    ):
        """Download Wind Simulation Task results

        Parameters
        ----------
        wind_simulation_task_id : str
            Id of wind simulation
        file : str, optional
            File of the results files to download, by default "results"
        output_name : str, optional
            Output file name to use if provided, else use same name as remote file, by default None
        output_dir : str, optional
            Output directory path, by default None

        Raises
        ------
        ValueError
            Raises error if file type is not in the valid file types
        """
        if not output_dir:
            output_dir = os.getcwd()
        if file and file not in VALID_DOWNLOAD_FILES:
            err_msg = f"File type <{file}> is not in the valid file types <{VALID_DOWNLOAD_FILES}>"
            raise ValueError(err_msg)

        download_url = f"{self.session.server_url}{self.URL}/{wind_simulation_task_id}/download_url"
        download_url += f"?file_path={file}" if file else ""
        wind_simulation_task_file_url = self.session.get_request(download_url).json()[
            "url"
        ]
        # NOTE: If provided, use given name, else take same name as remote
        if output_name:
            local_filename = output_name
        else:
            local_filename = os.path.basename(
                urlparse(wind_simulation_task_file_url).path
            )
        print(
            f"Fetch <{file}> data of simulation <{wind_simulation_task_id}> and store it at: <{local_filename}>"
        )
        file_request = self.session.get_request(wind_simulation_task_file_url)
        download_write_chunks(f"{output_dir}/{local_filename}", file_request)
