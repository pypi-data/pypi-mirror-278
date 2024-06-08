# Original author is Niels Rogge, source: https://github.com/NielsRogge/Transformers-Tutorials/blob/master/Table%20Transformer/Using_Table_Transformer_for_table_detection_and_table_structure_recognition.ipynb


import matplotlib.pyplot as plt


# colors for visualization
colors = ["red", "blue", "green", "yellow", "orange", "violet"]



def plot_results_unwr(pil_img, confidence, labels, boxes, id2label, filter=None, figsize=(32,20)): # prob, boxes):
    """
    confidence = [0.993, 0.927]
    labels = [0, 0] # 0 is the table class
    boxes = [[0.000, 0.000, 70.333, 20.333], # bounding boxes: xmin, ymin, xmax, ymax
                     [10.001, 0.001, 0.998, 0.998]]
    }"""
    # confidence = results["scores"].tolist()
    # labels = results["labels"].tolist()
    # boxes = results["boxes"].tolist()
    if id2label is None:
        id2label = {0: "table", 1: "table rotated"}
    plt.figure(figsize=figsize)
    plt.imshow(pil_img)
    ax = plt.gca()
    for cl, lbl, (xmin, ymin, xmax, ymax) in zip(confidence, labels, boxes):
        # cl = p.argmax()
        if filter is not None and lbl not in filter:
            continue
        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   fill=False, color=colors[lbl], linewidth=3))
        text = f'{id2label[lbl]}: {cl:0.2f}'
        ax.text(xmin, ymin, text, fontsize=15,
                bbox=dict(facecolor='yellow', alpha=0.5))
    plt.axis('off')
    plt.show()


def plot_results_orig(pil_img, results, id2label, filter=None): # prob, boxes):
    """
    results = {
    "scores": tensor([0.993, 0.927]),
    "labels": tensor([0, 0]), # this is always 0, for the table class
    "boxes": tensor([[0.000, 0.000, 70.333, 20.333], # bounding boxes: xmin, ymin, xmax, ymax
                     [10.001, 0.001, 0.998, 0.998]]),
    }"""
    plot_results_unwr(pil_img, results["scores"].tolist(), results["labels"].tolist(), results["boxes"].tolist(), id2label, filter=filter)
