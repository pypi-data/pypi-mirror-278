"""
GPT Vision to make Control Decisions
"""

from typing import Dict

import cv2
import numpy as np
import torch
from diffusers.schedulers.scheduling_ddpm import DDPMScheduler
from PIL import Image as PILImage

from general_navigation.models.factory import (
    get_default_config,
    get_model,
    get_weights,
)
from general_navigation.models.model_utils import model_step
from general_navigation.mpc import MPC
from general_navigation.schema.environment import DroneControls, DroneState


class GPTVision:
    def __init__(
        self,
        config: Dict = get_default_config(),
        device: str = "auto",
    ):
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"

        self.device = device
        self.config = config
        self.model = get_model(self.config)
        self.model = get_weights(self.config, self.model, self.device)

        if config["run_name"] == "nomad":
            self.noise_scheduler = DDPMScheduler(
                num_train_timesteps=config["num_diffusion_iters"],
                beta_schedule="squaredcos_cap_v2",
                clip_sample=True,
                prediction_type="epsilon",
            )

        self.model = self.model.to(device=self.device)

        self.context_queue = []
        self.context_size = config["context_size"]

        self.speed = 5.0  # m/s

        self.horizon = 6

        self.mpc = MPC(self.speed, 0.25, self.horizon)

        self.trajectory_history = []
        self.trajectory_history_size = 2

    def step(
        self,
        state: DroneState,
    ) -> DroneControls:
        # base64_image = encode_opencv_image(image)
        np_frame = state.image.cv_image()
        frame = cv2.cvtColor(np_frame, cv2.COLOR_BGR2RGB)
        frame = PILImage.fromarray(frame)
        gpt_controls = DroneControls(
            trajectory=[(0, 0), (0, 0)],
            trajectory_mpc=[(0, 0), (0, 0)],
            speed=0.0,
            steer=0.0,
        )

        if len(self.context_queue) < self.context_size + 1:
            self.context_queue.append(frame)
        else:
            self.context_queue.pop(0)
            self.context_queue.append(frame)

        # print("image:", np_frame.shape)
        # print("state:", str(state))

        trajectory = model_step(
            self.model,
            self.noise_scheduler,
            self.context_queue,
            self.config,
            self.device,
        )

        if trajectory is not None:
            self.trajectory_history.append(trajectory.tolist())

            if len(self.trajectory_history) > self.trajectory_history_size:
                self.trajectory_history.pop(0)

            gpt_controls.trajectory = np.mean(
                np.array(self.trajectory_history), axis=0
            )
            gpt_controls.trajectory = gpt_controls.trajectory[2:]
            gpt_controls.trajectory = gpt_controls.trajectory.tolist()
            gpt_controls.speed = self.speed

            accel, steer, traj_mpc = self.mpc.step(
                np.array(gpt_controls.trajectory),
                state.speed_ms(),
                state.steering_angle,
            )

            gpt_controls.steer = steer
            gpt_controls.trajectory_mpc = traj_mpc

        return gpt_controls
