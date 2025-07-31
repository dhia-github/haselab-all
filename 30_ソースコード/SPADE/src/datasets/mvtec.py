import os
import tarfile
from PIL import Image
from tqdm import tqdm
import urllib.request

import torch
from torch.utils.data import Dataset
from torchvision import transforms as T


URL = 'ftp://guest:GU.205dldo@ftp.softronics.ch/mvtec_anomaly_detection/mvtec_anomaly_detection.tar.xz'
CLASS_NAMES = ['bottle', 'cable', 'capsule', 'carpet', 'grid',
               'hazelnut', 'leather', 'metal_nut', 'pill', 'screw',
               'tile', 'toothbrush', 'transistor', 'wood', 'zipper']


class MVTecDataset(Dataset):
    def __init__(self, root_path='../data', class_name='bottle', is_train=True,
                 resize=256, cropsize=224):
        #    プログラムの前提条件をチェックするための**アサーション（Assertion）満たしていない場合メッセージとAssertionError**
        assert class_name in CLASS_NAMES, 'class_name: {}, should be in {}'.format(class_name, CLASS_NAMES)
        self.root_path = root_path
        self.class_name = class_name
        self.is_train = is_train
        self.resize = resize
        self.cropsize = cropsize
        self.mvtec_folder_path = os.path.join(root_path, 'mvtec_anomaly_detection')

        # download dataset if not exist
        self.download()

        # load dataset パスを指定 画像、ラベル、マスクのパスリスト
        self.x, self.y, self.mask = self.load_dataset_folder()

        # set transforms
        # self.transform_x = T.Compose([T.Resize(resize, Image.ANTIALIAS),
        #                               T.CenterCrop(cropsize),
        #                               T.ToTensor(),
        #                               T.Normalize(mean=[0.485, 0.456, 0.406],
        #                                           std=[0.229, 0.224, 0.225])])
        # self.transform_mask = T.Compose([T.Resize(resize, Image.NEAREST),
        #                                  T.CenterCrop(cropsize),
        #                                  T.ToTensor()])
        self.transform_x = T.Compose([T.Resize(resize, T.InterpolationMode.LANCZOS), # <- ANTIALIASの新しい書き方 size, method
                              T.CenterCrop(cropsize),
                              T.ToTensor(),
                              T.Normalize(mean=[0.485, 0.456, 0.406],
                                          std=[0.229, 0.224, 0.225])])
        self.transform_mask = T.Compose([T.Resize(resize, T.InterpolationMode.NEAREST), # <- こちらも新しい書き方に統一
                                 T.CenterCrop(cropsize),
                                 T.ToTensor()])



    def __getitem__(self, idx):
        # この段階ではまだパスを代入しているだけ
        x, y, mask = self.x[idx], self.y[idx], self.mask[idx]

        # ファイルパスを使って、画像ファイル画像を読み込み、変換を適用
        x = Image.open(x).convert('RGB')
        x = self.transform_x(x)

        if y == 0: #正常画像ならばマスクは不要なので黒塗り
            mask = torch.zeros([1, self.cropsize, self.cropsize])
        else:
            mask = Image.open(mask)
            mask = self.transform_mask(mask)





        return x, y, mask

    def __len__(self):
        return len(self.x)

    def load_dataset_folder(self):
        phase = 'train' if self.is_train else 'test'
        x, y, mask = [], [], []

        img_dir = os.path.join(self.mvtec_folder_path, self.class_name, phase)
        gt_dir = os.path.join(self.mvtec_folder_path, self.class_name, 'ground_truth')

        #フォルダ内にある全てのファイル名とサブディレクトリ名をリストとして返し、ソート
        img_types = sorted(os.listdir(img_dir))
        for img_type in img_types:

            # load images
            img_type_dir = os.path.join(img_dir, img_type)
            if not os.path.isdir(img_type_dir):
                continue
            img_fpath_list = sorted([os.path.join(img_type_dir, f)
                                     for f in os.listdir(img_type_dir)
                                     if f.endswith('.png')])  # 画像ファイルの拡張子がpngのもの
            x.extend(img_fpath_list) #既存のリストxの末尾に追加

            # load gt labels
            if img_type == 'good':
                y.extend([0] * len(img_fpath_list))
                mask.extend([None] * len(img_fpath_list))
            else:
                y.extend([1] * len(img_fpath_list))
                gt_type_dir = os.path.join(gt_dir, img_type)#特定のマスク画像群パス

                #フルパスからファイル名と拡張子部分だけを取り出しbasenameで、splittext "split extension"（拡張子を分割してリストにその０要素目）

                img_fname_list = [os.path.splitext(os.path.basename(f))[0] for f in img_fpath_list]
                gt_fpath_list = [os.path.join(gt_type_dir, img_fname + '_mask.png')
                                 for img_fname in img_fname_list]
                mask.extend(gt_fpath_list)

        assert len(x) == len(y), 'number of x and y should be same'

        return list(x), list(y), list(mask)

    def download(self):
        """Download dataset if not exist"""

        if not os.path.exists(self.mvtec_folder_path):
            tar_file_path = self.mvtec_folder_path + '.tar.xz'
            if not os.path.exists(tar_file_path):
                download_url(URL, tar_file_path)
            print('unzip downloaded dataset: %s' % tar_file_path)
            tar = tarfile.open(tar_file_path, 'r:xz')  #レトルトカレーのパウチを開ける
            tar.extractall(self.mvtec_folder_path)   #指定されたフォルダに展開
            tar.close()

        return


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

# # withを使わない場合（手動での後片付けが必要）
# t = DownloadProgressBar(...)
# try:
#     urllib.request.urlretrieve(..., reporthook=t.update_to)
# finally:
#     t.close() # 必ず後片付け処理を呼ぶ必要がある