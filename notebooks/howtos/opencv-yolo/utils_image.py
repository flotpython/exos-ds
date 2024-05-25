import cv2
# import time

def show_image(img, *, window_name="window", x_window=0, y_window=0,
               on_top=True, store_in_filename=None):
    '''
    show image img in a window at position (x_window, y_window) on screen
    put the image on top-most front of other windows if requested
    stores the image in a file if requested

    press any keyboard key or mouse click to end the function and delete the window
    '''
    if img is None:
        return

    done_waiting = False

    # https://pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/
    def handle_mouse_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            nonlocal done_waiting
            done_waiting = True

    # https://stackoverflow.com/questions/6116564/destroywindow-does-not-close-window-on-mac-using-python-and-opencv
    cv2.startWindowThread()

    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, handle_mouse_click)

    cv2.imshow(window_name, img)
    cv2.moveWindow(window_name, x_window, y_window)
    if on_top:
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

    print("waiting for any character or a click to close the window...", end='')

    while True:
        # command-w or alt-f4
        if not cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE):
            done_waiting = True
        if done_waiting:
            break
        # a key was pressed within 40ms
        if k := cv2.waitKey(40) >= 0:
            print(f" got {k=}", end="")
            done_waiting = True

    print(f" ok")
    if store_in_filename:
        cv2.imwrite(store_in_filename, img)
    cv2.destroyAllWindows()
    # needed on macOS at least, see same SO post as above
    cv2.waitKey(1)


