import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def load_image(file_name, number):
    img = Image.open(file_name)
    img.load()
    print(img.format, img.mode, img.size)
    bw = img.convert('L')

    #print(bw.size)
    bw_data = np.array(bw).astype('int32')
    #print(bw_data.shape)
    bins = np.array(range(0,255))
    counts, pixels =np.histogram(bw_data, bins)
    pixels = pixels[:-1]
    plt.bar(pixels, counts, align='center')
    plt.savefig('histogram' +str(number) + '.png')
    plt.xlim(-1, 256)
    plt.show()

    total_counts = np.sum(counts)
    # assert total_counts == bw_data.shape[0]*bw_data.shape[1]

    return bins, counts, pixels, bw_data, total_counts

def otsu(gray, bins, total_counts):
    pixel_number = gray.shape[0] * gray.shape[1]
    mean_weigth = 1.0/total_counts
    his, bins = np.histogram(gray, np.array(range(0, 256)))
    final_thresh = -1
    final_value = -1
    for t in bins[1:-1]: # This goes from 1 to 254 uint8 range (Pretty sure wont be those values)
        Wb = np.sum(his[:t]) * mean_weigth
        Wf = np.sum(his[t:]) * mean_weigth

        mub = np.mean(his[:t])
        muf = np.mean(his[t:])

        value = Wb * Wf * (mub - muf) ** 2

        # print("Wb", Wb, "Wf", Wf)
        # print("t", t, "value", value)

        if value > final_value:
            final_thresh = t
            final_value = value
            #print("new t = ", t)
    final_img = gray.copy()
    print(final_thresh)
    final_img[gray > final_thresh] = 255
    final_img[gray < final_thresh] = 0
    return final_img



def main():
    for i in range(1,16):
        if i < 10:
            file_name = '0' + str(i) + '.jpg'
        else:
            file_name = str(i) + '.jpg'
        bins, counts, pixels, bw_data, total_counts = load_image(file_name, i)
        final_img = otsu(bw_data, bins, total_counts)
        plt.imshow(final_img)

        if i < 10:
            figname = '0' + str(i) + '_otsu.jpg'
        else:
            figname = str(i) + '_otsu.jpg'

        plt.savefig(figname)
        plt.show()
    print("----END!----")



if __name__ == "__main__":
    main()
