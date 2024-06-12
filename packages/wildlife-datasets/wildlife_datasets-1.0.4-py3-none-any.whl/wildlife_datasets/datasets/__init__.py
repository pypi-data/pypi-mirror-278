from .datasets import DatasetFactory
from .datasets import AAUZebraFish
from .datasets import AerialCattle2017
from .datasets import ATRW
from .datasets import BelugaID, BelugaIDv2
from .datasets import BirdIndividualID
from .datasets import BirdIndividualIDSegmented
from .datasets import CatIndividualImages
from .datasets import CTai
from .datasets import CZoo
from .datasets import CowDataset
from .datasets import Cows2021, Cows2021v2
from .datasets import DogFaceNet
from .datasets import Drosophila
from .datasets import FriesianCattle2015, FriesianCattle2015v2
from .datasets import FriesianCattle2017
from .datasets import GiraffeZebraID
from .datasets import Giraffes
from .datasets import GreenSeaTurtles
from .datasets import HappyWhale
from .datasets import HumpbackWhaleID
from .datasets import HyenaID2022
from .datasets import IPanda50
from .datasets import LeopardID2022
from .datasets import LionData
from .datasets import MacaqueFaces
from .datasets import MPDD
from .datasets import NDD20, NDD20v2
from .datasets import NOAARightWhale
from .datasets import NyalaData
from .datasets import OpenCows2020
from .datasets import PolarBearVidID
from .datasets import SealID
from .datasets import SealIDSegmented
from .datasets import SeaStarReID2023
from .datasets import SeaTurtleID2022
from .datasets import SeaTurtleIDHeads
from .datasets import SMALST
from .datasets import StripeSpotter
from .wildlife_reid_10k import WildlifeReID10k
from .datasets import WhaleSharkID
from .datasets import ZindiTurtleRecall
from .metadata import Metadata
from .utils import get_image

names_all = [
    AAUZebraFish,
    AerialCattle2017,
    ATRW,
    BelugaIDv2,
    BirdIndividualID,
    BirdIndividualIDSegmented,
    CatIndividualImages,
    CTai,
    CZoo,
    CowDataset,
    Cows2021v2,
    DogFaceNet,
    Drosophila,
    FriesianCattle2015v2,
    FriesianCattle2017,
    GiraffeZebraID,
    Giraffes,
    GreenSeaTurtles,
    HappyWhale,
    HumpbackWhaleID,
    HyenaID2022,
    IPanda50,
    LeopardID2022,
    LionData,
    MacaqueFaces,
    MPDD,
    NDD20v2,
    NOAARightWhale,
    NyalaData,
    OpenCows2020,
    PolarBearVidID,
    SealID,
    SealIDSegmented,
    SeaStarReID2023,
    SeaTurtleID2022,
    SeaTurtleIDHeads,
    SMALST,
    StripeSpotter,
    WhaleSharkID,
    ZindiTurtleRecall,
]

names_wild = [
    BelugaIDv2,
    GiraffeZebraID,
    GreenSeaTurtles,
    HappyWhale,
    HumpbackWhaleID,
    HyenaID2022,
    LeopardID2022,
    NDD20v2,
    NOAARightWhale,
    NyalaData,
    SealID,
    SeaTurtleID2022,
    StripeSpotter,
    WhaleSharkID,
]

names_small = [
    AerialCattle2017,
    BelugaIDv2,
    CTai,
    CZoo,
    DogFaceNet,
    FriesianCattle2015v2,
    FriesianCattle2017,
    IPanda50,
    GreenSeaTurtles,
    MacaqueFaces,
    MPDD,
    NyalaData,
    PolarBearVidID,
    SeaTurtleIDHeads,
    StripeSpotter,
]

names_cows = [
    AerialCattle2017,
    CowDataset,
    Cows2021v2,
    FriesianCattle2015v2,
    FriesianCattle2017,
    OpenCows2020,
]

names_dogs = [
    DogFaceNet,
    MPDD,
]

names_giraffes = [
    GiraffeZebraID,
    Giraffes,
    SMALST,
    StripeSpotter,
]

names_primates = [
    CTai,
    CZoo,
    MacaqueFaces,
]

names_turtles = [
    GreenSeaTurtles,
    SeaTurtleIDHeads,
    ZindiTurtleRecall,
]

names_whales = [
    BelugaIDv2,
    HappyWhale,
    HumpbackWhaleID,
    NDD20v2,
    NOAARightWhale,
    WhaleSharkID,
]
