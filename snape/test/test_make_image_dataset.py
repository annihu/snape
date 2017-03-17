
import shutil
from snape.make_image_dataset import *
from snape.make_image_dataset import _ImageNet, _ImageGrabber


def test_make_image_dataset():
    # todo: tests for this main function, mostly test user inputs
    pass


class TestImageNet:

    def test_sample_synset_links(self):
        n = 5
        wnid = 'n02114855'
        im_dir = os.getcwd() + '/im_dir/'
        os.mkdir(im_dir)
        try:
            _ImageNet(1).sample_synset_links(wnid, n, im_dir)
            n_images = len(os.listdir(im_dir + '/' + wnid))
            assert n == n_images, "Did not download n images"
            assert wnid in os.listdir(im_dir), "Did not get the requested synset"
        except:
            raise
        finally:
            shutil.rmtree(im_dir)

    def test_get_images(self):
        n = 5
        im_dir = os.getcwd() + '/im_dir/'
        os.mkdir(im_dir)
        try:
            _ImageNet(1).get_images(n, im_dir)
            sub_dir = im_dir + os.listdir(im_dir)[0]
            n_images = len(os.listdir(sub_dir))
            assert n == n_images, "Did not download n images"
        except:
            raise
        finally:
            shutil.rmtree(im_dir)

    def test_get_ilsvrc_1000_synsets(self):
        synsets = _ImageNet.get_ilsvrc_1000_synsets()
        assert len(synsets) == 1000, "ILSVRC page parsed incorrectly"

    def test_get_synset_image_links(self):
        wnid = 'n02114855'
        links = _ImageNet.get_synset_image_links(wnid)
        assert len(links) > 0, "Did not return any image links"

    def test_retrieve_class_counts(self):
        class_counts = _ImageNet.retrieve_class_counts()
        assert isinstance(class_counts, pd.core.frame.DataFrame), "Class counts not returned in a dataframe"


class TestImageGrabber:

    def test_download_image(self):
        good_url = "http://farm4.static.flickr.com/3290/2998414960_01dd35d094.jpg"
        good_im_path = "ducky.jpg"
        _ImageGrabber().download_image(good_url, good_im_path)
        good_im_type = imghdr.what(good_im_path)
        os.remove(good_im_path)
        assert good_im_type is not None
        bad_url = "https://mckinleyleather.com/image/130963084.jpg"
        bad_im_path = "no_ducky.jpg"
        _ImageGrabber().download_image(bad_url, bad_im_path)
        is_file = os.path.isfile(bad_im_path)
        assert not is_file

    def test_catch_unavailable_image(self):
        good_url = "http://farm4.static.flickr.com/3290/2998414960_01dd35d094.jpg"
        good_img_data = requests.get(good_url)
        assert not _ImageGrabber.catch_unavailable_image(good_img_data), "The good image tested was found to be bad"
        stale_url = "https://mckinleyleather.com/image/130963084.jpg"
        stale_img_data = requests.get(stale_url)
        assert _ImageGrabber.catch_unavailable_image(stale_img_data), "The stale image tested was found to be good"
        junk_url = "http://farm4.static.flickr.com/3225/2806850016_9bf939037e.jpg"
        junk_img_data = requests.get(junk_url)
        assert _ImageGrabber.catch_unavailable_image(junk_img_data),  "The junk image tested was found to be good"


class TestOpenImages:
    pass


class TestGoogleSearch:
    pass
