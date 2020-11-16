### CZ4042 Project AY20/21 SEM 1
This project is a modification of the original [MMALNet](https://arxiv.org/abs/2003.09150) by Fan Zhang, Meng Li, Guisheng Zhai, and Yizhao Liu.

The experiment is performed on the CompCars dataset.

For assessing the project, please refer to the sections on `Installing Dependencies` and `Testing MMALNet`

### Installing Dependencies
Instructions for setting up the required conda environment (pip can be used as well):
- Create a conda environment: `conda create --name ENV_NAME`
- Ensure conda environment is activated: `conda activate ENV_NAME`
- Install Python 3.7.x: `conda install python=3.7`
- Install PyTorch and TorchVision via pytorch channel: `conda install pytorch torchvision -c pytorch`
- Install other packages: `conda install numpy pandas tqdm pillow imageio scikit-learn scikit-image`
- Install TensorboardX: `conda install tensorboardx -c conda-forge`
- Install Tensorboard: `conda install tensorboard`
- Install OpenCV: `conda install opencv`
- Install RandAug: `pip install git+https://github.com/ildoonet/pytorch-randaugment`
	- This package must be installed via `pip`
	- To install this package without git+, download the repo and simply install the downloaded .zip file: `pip install <zipfile name>.zip`
	- More details on RandAug can be found in this [paper](https://arxiv.org/abs/1909.13719)

### Running MMALNet for Fine Tuning`num_classes`
This section is not required for testing the model but indicates the workflow used during training
1. Download the [pretrained model of ResNet-50](https://download.pytorch.org/models/resnet50-19c8e357.pth) and move it to `models/pretrained`
	- Other ResNets like ResNet-152 can also be used if desired
	
2. For cases where GPU memory is insufficient: tweak `N_list`, or lower `batch_size`, these parameters can be found in `config.py`
	- The parameter N_list is N1, N2, N3 in the [original paper](https://arxiv.org/pdf/2003.09150v3.pdf) and you can adjust them according to GPU memory
	- batch_size can be lowered to 3 or below
	
3. Download the `CompCars` dataset. The instructions are available [here](http://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/)
	- Add the `image` folder from the unzipped CompCars data: 
		- i.e. Move `CompCars/data/image/` into `datasets/CompCars`, it should reside in the same directory as `prepare-data_csv.ipynb`
		- The other folders like `label`, `misc`, etc. are not necessary
		
4. Ensure `config.py` variables are set properly
	- `eval_trainset`
		- This is to allow evaluation metrics to be obtained for the training
		- If no training metrics are desired, set to `False` to save training time
	- `set`
		- Set to `CompCars` to load CompCars dataset; Can be set to other datasets like CUB200, etc.
	- `rand_aug`
		- Set to `True` if RandAug (Random Augmentation) is to be used for training, else set to `False`
		- Does not affect testing as RandAug is not used in testing phase.
	- `num_folds`
		- Set the number of folds for Stratified K-Folds cross validation
	- `start_from_fold`
		- Change this to the fold you wish to begin from; to be used when resuming training.
		- NOTE: that this value may cause unexpected behaviour if improperly set; e.g. if you wish to resume training from fold 2 (i.e. stopped training at fold 2), then set `start_from_fold=2`
	- `patience`
		- Training stops if more than the specified number of epochs elapsed without an improvement in specified metric
		- Specified metric for our purposes on CompCars dataset is the local_accuracy metric
	- `patience_counter`
		- This should be initialised to 0
	- `num_classes`
		- For `CompCars` dataset:
			- Predict `car_make` - set to 75
			- Predict `car_model` - set to 431
			- Multi-Task Learning on both `car_model` and `car_make` - set to a tuple of (431, 75), with (`car_model`, `car_make`)
	
5. Run `python tuning.py` to commence training
	- Train dataset will be split into training and validation sets (80:20), and Stratified K-Folds is performed for k=5
		- To be used for hyperparameter tuning or evaluating model modifications
	- During training, the `tensorboardx` log file and epoch checkpoints will be saved in their respective folds' directories
	- `tensorboardx` log files can be viewed via `tensorboard`
	
6. Run `python train.py` to train finalised model
	- Training and testing will be performed on the original (50:50) data split

### Testing MMALNet
1. Ensure variables are set properly in `test.py`
	- Ensure `set` variable is `CompCars`, for properly assessing our saved model trained on the `CompCars` dataset
	
	- Ensure `num_classes` and `multitask` variables is set accordingly:
		- `multitask` parameter must be changed (True/False) in `config.py`
		- For setting `num_classes` on the `CompCars` dataset:
			- Predict `car_make` - set `num_classes` to 75 and set `multitask` to False
			- Predict `car_model` - set `num_classes` to 431 and set `multitask` to False
			- Multi-Task Learning on both `car_model` and `car_make` - set `num_classes` to a tuple of (431, 75) which is of the format (`car_model`, `car_make`), and set `multitask` to True
			
	- Download the desired trained model provided and place the model in the location indicated by `pth_path` (i.e. `./models`)
		- The available saved models are from training to predict:
			- `car_make` only: LINK
			- `car_model` only: LINK
			- Multi-Task learning on both `car_make` and `car_model` attributes: LINK
			- `car_model` with `RandAug` (N:1, M:15): LINK
			
		- The model filename indicates the epoch that the model with the best `local_accuracy` was saved at
			- Early Stopping was performed on the `local_accuracy` metric of the `MMALNet` during training
			
	- Note that `pth_path` must be changed to point to the saved model in `test.py`
		- Saved model name can be renamed if desired, but `pth_path` must be updated accordingly
		- e.g. if trained model filename is `multitask_epoch1.pth`, then ensure `pth_path` properly reflects the saved model's filename: `./models/multitask_epoch1.pth`
		
2. Run `python test.py` to test the model
	- NOTE: the testloader should be modified to contain only unseen data for accurate evaluation of model accuracy
	- For cases where GPU memory is insufficient: lower `batch_size`