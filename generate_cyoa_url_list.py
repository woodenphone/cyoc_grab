#-------------------------------------------------------------------------------
# Name:        module1
# Purpose: Generate URL list for wget/wpull/httrack
#
# Author:      User
#
# Created:     17/06/2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import os



def generate_chapter_list(list_path, low_chapter_id, high_chapter_id):
    with open(list_path, 'w') as f:
        for current_id in xrange(low_chapter_id,high_chapter_id):
            line_str = 'http://www.cyoc.net/interactives/chapter_%s.html\n' % (current_id)
            f.write(line_str)
    return


def generate_outline_list(list_path, low_chapter_id, high_chapter_id):
    with open(list_path, 'w') as f:
        for current_id in xrange(low_chapter_id,high_chapter_id):
            line_str = 'http://www.cyoc.net/interactives/story_%s/outline.html\n' % (current_id)
            f.write(line_str)
    return


def main():
    output_folder = 'debug'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    generate_outline_list(
        list_path = os.path.join(output_folder, 'cyoa_outline_urls.txt'),
        low_chapter_id = 1,
        high_chapter_id = 100
    )

    generate_chapter_list(
        list_path = os.path.join(output_folder, 'cyoa_chapter_urls.txt'),
        low_chapter_id = 100000,
        high_chapter_id = 101000
    )

if __name__ == '__main__':
    main()
