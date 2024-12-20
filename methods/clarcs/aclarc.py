import lightning as L
import torch

from .clarc import CLARC
from .hooks import add_clarc_hook


class ACLARC(CLARC):
    def __init__(
        self, model: L.LightningModule, experiment_name: str, device: str, **kwargs
    ) -> None:
        super().__init__(model, experiment_name, device)
        self.lightning_model = model

    def apply_model_correction(
        self,
        cav_layers: list[str],
        dataloader: torch.utils.data.DataLoader,
        logger: object | bool = False,
        fine_tune_epochs: int = 1,
        alpha: float = 1.0,
        **kwargs,
    ) -> None:
        for cav_layer in cav_layers:
            hook = add_clarc_hook(
                self.model,
                self.cav[cav_layer],
                self.mean_act_a[cav_layer],
                cav_layer,
                alpha,
            )
            self.hooks.append(hook)

        # Make sure model is in training mode
        self.model.train()

        trainer = L.Trainer(
            max_epochs=fine_tune_epochs, logger=logger, log_every_n_steps=1
        )
        trainer.fit(self.lightning_model, dataloader)

        # Go back to eval mode
        self.model.eval()

        # Remove hooks
        self.remove_hooks()
