#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     17/06/2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def generate_story_list(list_path, low_chapter_id, high_chapter_id):
    with open(list_path, 'w') as f:
        for current_id in xrange(low_chapter_id,high_chapter_id):
            line_str = 'http://www.cyoc.net/modules.php?op=modload&name=Stories&file=article&sid=%s&mode=nested&order=0&thold=-1\n' % (current_id)
            f.write(line_str)
    return


def main():
    output_folder = 'debug'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    generate_story_list(
        list_path = os.path.join(output_folder, 'story_urls.txt'),
        low_chapter_id = 1,
        high_chapter_id = 2500
    )


if __name__ == '__main__':
    main()