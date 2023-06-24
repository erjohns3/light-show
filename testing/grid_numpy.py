import time
import serial
import random
import math
import signal
import sys
import numpy as np


def signal_handler(sig, frame):
    print('SIG Handler: ' + str(sig), flush=True)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


grid_serial = serial.Serial(
    port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
    baudrate = 2000000,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1,
    write_timeout=0
)

GRID_ROW_LENGTH = 20
GRID_COL_LENGTH = 32

GRID_ROW = np.arange(GRID_ROW_LENGTH)
GRID_COL = np.arange(GRID_COL_LENGTH)

time_a = time.time()*1000

zero = np.ones((GRID_ROW_LENGTH, GRID_COL_LENGTH, 3))
grid = np.array(zero, np.single)
# grid = np.array((GRID_ROW_LENGTH, GRID_COL_LENGTH, 3))

grid_address = np.array(zero, np.short)

grid_lut = np.array([0])

time_b = time.time()*1000

grid[:, 0:15] = [1, 2, 3]

np.nonzero(grid[:,:,0]) 

indeces = np.nonzero(grid[:,:,0])

pos_x = 9.5
pos_y = 15.5

r = np.sqrt(np.square(indeces[0]-pos_x) + np.square(indeces[1]-pos_y))

# print(indeces)

time_c = time.time()*1000

# print(grid[0])

print(f'init: {time_b - time_a}, zero: {time_c - time_b}')



grid_index = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, -1, -1], 
    [63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 50, 49, 48, 46, 45, 44, 43, 42, 40, 39, 38, 37, 36, 35, 34, 33, 32, -1, -1], 
    [64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 81, 82, 83, 84, 85, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, -1], 
    [127, 126, 125, 124, 123, 122, 121, 120, 119, 118, 117, 116, 115, 114, 113, 112, 111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101, 100, 99, 98, 97, -1], 
    [128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159], 
    [191, 190, 189, 188, 187, 186, 185, 184, 183, 182, 181, 180, 179, 178, 177, 176, 175, 174, 173, 172, 171, 170, 169, 168, 167, 166, 165, 164, 163, 162, 161, 160], 
    [192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223], 
    [255, 254, 253, 252, 251, 250, 249, 248, 247, 246, 245, 244, 243, 242, 241, 240, 239, 238, 237, 236, 235, 234, 233, 232, 231, 230, 229, 228, 227, 226, 225, 224], 
    [256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287], 
    [319, 318, 317, 316, 315, 314, 313, 312, 311, 310, 309, 308, 307, 306, 305, 304, 303, 302, 301, 300, 299, 298, 297, 296, 295, 294, 293, 292, 291, 290, 289, 288], 
    [320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351], 
    [383, 382, 381, 380, 379, 378, 377, 376, 375, 374, 373, 372, 371, 370, 369, 368, 367, 366, 365, 364, 363, 362, 361, 360, 359, 358, 357, 356, 355, 354, 353, 352], 
    [384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415], 
    [447, 446, 445, 444, 443, 442, 441, 440, 439, 438, 437, 436, 435, 434, 433, 432, 431, 430, 429, 428, 427, 426, 425, 424, 423, 422, 421, 420, 419, 418, 417, 416], 
    [448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479], 
    [511, 510, 509, 508, 507, 506, 505, 504, 503, 502, 501, 500, 499, 498, 497, 496, 495, 494, 493, 492, 491, 490, 489, 488, 487, 486, 485, 484, 483, 482, 481, 480], 
    [512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543], 
    [575, 574, 573, 572, 571, 570, 569, 568, 567, 566, 565, 564, 563, 562, 561, 560, 559, 558, 557, 556, 555, 554, 553, 552, 551, 550, 549, 548, 547, 546, 545, 544], 
    [576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607], 
    [639, 638, 637, 636, 635, 634, 633, 632, 631, 630, 629, 628, 627, 626, 625, 624, 623, 622, 621, 620, 619, 618, 617, 616, 615, 614, 613, 612, 611, 610, 609, 608]
]

def grid_pack():
    for x in range(GRID_ROW_LENGTH):
        for y in range(GRID_COL_LENGTH):
            index = grid_index[x][y] * 3
            grid_msg[index] = grid[x][y][0]
            grid_msg[index + 1] = grid[x][y][1]
            grid_msg[index + 2] = grid[x][y][2]


def grid_reset():
    global grid
    grid = np.zeros((GRID_ROW_LENGTH, GRID_COL_LENGTH, 3))

# for x in range(GRID_ROW_LENGTH):
#     grid_index[x] = [0]*GRID_COL_LENGTH
#     for y in range(GRID_COL_LENGTH):
#         if x % 2 == 0:
#             index = (x * GRID_COL_LENGTH) + y
#             grid_index[x][y] = index
#         else:
#             index = ((x+1) * GRID_COL_LENGTH) - 1 - y
#             grid_index[x][y] = index

grid_msg = [0] * (GRID_COL_LENGTH * GRID_ROW_LENGTH * 3)

while True:
    time_a = time.time()*1000
    
    grid_reset()

    time_b = time.time()*1000

    # period = 3

    # pos = (time.time() % period) / period

    # min(0.05 / ((abs((y / (GRID_COL_LENGTH - 1)) - pos) % 1) ** 2), 255)

    # d = abs((y / (GRID_COL_LENGTH - 1)) - pos) + abs((y / (GRID_COL_LENGTH - 1)) - pos - 1)

    for y in range(GRID_COL_LENGTH):
        for x in range(GRID_ROW_LENGTH):
            r = ((x**2) + (y**2))**0.5
            power = int(127 * math.sin(r) + 128)
            grid[x][y][0] = 170
            grid[x][y][1] = 170
            grid[x][y][2] = 170

    time_c = time.time()*1000

    # for i in range(0, len(grid_msg), 3):
    #     grid_msg[i] = 0
    # grid_msg[(num*3)%640] = 255

    grid_pack()

    time_d = time.time()*1000

    msg = bytes(grid_msg)

    # print(msg)

    time_e = time.time()*1000

    grid_serial.write(msg)

    time_f = time.time()*1000
    print(f'A: {time_e - time_a},  B: {time_c - time_b},E: {time_f - time_e}')
    time.sleep(1)
    