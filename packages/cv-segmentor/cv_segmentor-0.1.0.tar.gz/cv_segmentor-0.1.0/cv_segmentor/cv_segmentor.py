class CV_Segmentor(object):

    def __init__(self, name):
        self.name = name

    # Params
    # @image: numpy.ndarray((height, width, channels=3))
    # Return
    # @masks: numpy.ndarray((height * width))
    # @time_records: numpy.ndarray((n))
    def segment(self, image):
        raise NotImplementedError()