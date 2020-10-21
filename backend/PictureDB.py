#!/usr/bin/python3
import os
import re

# read in the unique pictures file, parse into date, time, cksum and filename.
# count the first 3 as the id.

class PictureDB(object):
    unique_pictures_file = 'data/unique_pictures_sorted'
    tags_file = 'data/tags'
    uri_root = '/api/v1/pictures'

    webserver_picture_root = os.environ.get('WEBSERVER_PICTURE_ROOT', 'http://localhost/Pictures')

    def make_id(self, picture):
        return " ".join(picture[0:3])

    def make_value(self, picture):
        # take off newline and surrounding quotes
        return " ".join(picture[3:]).rstrip().strip('"')

    def get_tags(self):
        # the tags file is a log, where we always append the latest change
        # so reading it through will overwrite old values with newer, which is OK
        tags = {}
        try:
            fh = open(self.tags_file, "r", encoding="utf-8")
            for line in fh:
                items = line.split(' ', 4)
                date = items[0]
                time = items[1]
                cksum = items[2]
                id = self.make_id(items)
                # tag list can contain spaces, last part will have newline
                tags_field = self.make_value(items)
                tags[id] = tags_field
            fh.close()
        except FileNotFoundError:
            pass
        return tags

    def get_unique_pictures(self):
        pictures = []
        fh = open(self.unique_pictures_file, "r", encoding="utf-8")
        for line in fh:
            items = line.split(' ', 4)
            date = items[0]
            time = items[1]
            cksum = items[2]
            # filenames can contain spaces, last part will have newline
            name = self.webserver_picture_root + self.make_value(items)

            pictures.append([date, time, cksum, name])
        fh.close()

        return pictures

    def get_pictures(self):
        tags = self.get_tags()
        unique_pictures = self.get_unique_pictures()
        pictures = []
        for picture in unique_pictures:
            id = self.make_id(picture)
            # add the tags from above and remeber
            if id not in tags:
                tags[id] = ''
            picture.append(tags[id])
            pictures.append(picture)
        return pictures

    # filter on a single positive or negative term
    def get_filtered_pictures(self, filter_string = ''):
        # if the filter_string starts with '!', take it off but reverse sense
        m = re.match('^!(.*)', filter_string)
        reverse = False
        if m:
            reverse = True
            filter_string = m.group(1)
        pictures = []
        for picture in self.get_pictures():
            if reverse:
                    if (filter_string not in picture[4]):
                        pictures.append(picture)
            else:
                    if (filter_string in picture[4]):
                        pictures.append(picture)
        return pictures

    # creates the array, sets first and last
    def set_up_links(self, pictures, filter_string, page_size):
        response = { 'links': {} }
        # can't have a first or last if no pictures in filter
        if 1 < len(pictures):
            first = self.make_id(pictures[0])
            last = self.make_id(pictures[-1])
            response['links']['first'] = self.uri_root \
                + '?range_start=' + first \
                + '&range_end=' + last \
                + '&page_starts_at=' + first \
                + '&filter_string=' + filter_string \
                + '&page_size={}'.format(page_size)
            response['links']['last'] = self.uri_root \
                + '?range_start=' + first \
                + '&range_end=' + last \
                + '&page_ends_at=' + last \
                + '&filter_string=' + filter_string \
                + '&page_size={}'.format(page_size)
            return (response, first, last)
        return (response, "", "") # empty


    def fill_in_links(self, response, first, last, filter_string, page_size, page):
        response['data'] = page
        if 1 < len(page):
            pfirst = self.make_id(page[0])
            plast = self.make_id(page[-1])
            response['links']['before'] = self.uri_root \
                + '?range_start=' + first \
                + '&range_end=' + last \
                + '&page_ends_before=' + pfirst \
                + '&filter_string=' + filter_string \
                + '&page_size={}'.format(page_size)
            response['links']['after'] = self.uri_root \
                + '?range_start=' + first \
                + '&range_end=' + last \
                + '&page_starts_after=' + plast \
                + '&filter_string=' + filter_string \
                + '&page_size={}'.format(page_size)
        return response

    # more complicated now, there is a range and a page within the range
    # expect one of starts_at, starts_afer, ends_before, ends_at
    # if none, just start at the beginning
    # TODO - enums in python
    def get_a_page_of_filtered_pictures(self, 
            range_start = '0000', 
            range_end = '99999', 
            mode = 'page_starts_at',
            where = '0000',
            page_size = 10, 
            filter_string = ''):

        # get all pictures that meet our filter
        pictures = self.get_filtered_pictures(filter_string)
        pic_range = []
        # but then refine that set to be all pictures that meet our range
        for p in pictures:
            id = self.make_id(p)
            if range_end >= id >= range_start:
                pic_range.append(p)
        # we now know start, end of range, so start building links
        (response, first, last) = self.set_up_links(pic_range, filter_string, page_size)
        # but now find the individual page we want
        page = []
        for p in pic_range:
            id = self.make_id(p)
            if 'page_starts_at' == mode:
                if where <= id:
                    page.append(p)
            elif 'page_starts_after' == mode:
                if where < id:
                    page.append(p)
            elif 'page_ends_before' == mode:
                if where > id:
                    page.append(p)
            elif 'page_ends_at' == mode:
                if where >= id:
                    page.append(p)
            else:
                raise Exception('bad mode: ' + mode)

        # we want the page at the end of our set
        if 'page_ends' in mode:
            return self.fill_in_links(response, first, last, filter_string, page_size, page[-page_size:])
        # otherwise, just return beginning of our set 
        return self.fill_in_links(response, first, last, filter_string, page_size, page[:page_size])

    # given a changed tag, append a record to the tag file
    def patch_tags(self, id, tags):
        fh = open(self.tags_file, "a", encoding="utf-8")
        fh.write(id + ' "' + tags + "\"\n")
        fh.close()

if __name__ == '__main__':
    pdb = PictureDB()

    print("beginning of range with page size 1")
    pictures = pdb.get_a_page_of_filtered_pictures('0000', '99999', 'page_starts_at', '0000', 1, '')
    for x in pictures['data']:
        print(x)
    pictures = pdb.get_a_page_of_filtered_pictures('0000', '99999', 'page_starts_after', '0000', 1, '')
    for x in pictures['data']:
        print(x)

    print("end of range with page size 1")
    pictures = pdb.get_a_page_of_filtered_pictures('0000', '99999', 'page_ends_before', '99999', 1, '')
    for x in pictures['data']:
        print(x)
    pictures = pdb.get_a_page_of_filtered_pictures('0000', '99999', 'page_ends_at', '99999', 1, '')
    for x in pictures['data']:
        print(x)

    print("beginning of page with page size 1")
    pictures = pdb.get_a_page_of_filtered_pictures('2004', '2006', 'page_starts_at', '2005', 1, '')
    for x in pictures['data']:
        print(x)
    pictures = pdb.get_a_page_of_filtered_pictures('2004', '2006', 'page_starts_after', '2005', 1, '')
    for x in pictures['data']:
        print(x)

    print("end of page with page size 1")
    pictures = pdb.get_a_page_of_filtered_pictures('2004', '2006', 'page_ends_before', '2005', 1, '')
    for x in pictures['data']:
        print(x)
    pictures = pdb.get_a_page_of_filtered_pictures('2004', '2006', 'page_ends_at', '2005', 1, '')
    for x in pictures['data']:
        print(x)

