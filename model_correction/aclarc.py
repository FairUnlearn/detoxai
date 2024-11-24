import lightning as L

from .base_model_correction import ModelCorrectionMethod
from .hooks import add_clarc_hook


class ACLARC(ModelCorrectionMethod):
    def __init__(self, model, dataloader, experiment_name, layers, device):
        super().__init__(model, dataloader, experiment_name, layers, device)

        # Make sure that model

    def apply_model_correction(
        self,
        cav_layer: str,
        lightning_model,
        dataloader_train,
        logger,
        fine_tune_epochs: int = 1,
        alpha: float = 1.0,
    ) -> None:
        self.hooks = add_clarc_hook(
            self.model, self.cav, self.mean_act_a, [cav_layer], alpha
        )

        # Make sure model is in training mode
        self.model.train()

        trainer = L.Trainer(
            max_epochs=fine_tune_epochs, logger=logger, log_every_n_steps=1
        )
        trainer.fit(lightning_model, dataloader_train)

        # Go back to eval mode
        self.model.eval()

        # Remove hooks
        self.remove_hooks()
