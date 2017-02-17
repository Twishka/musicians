# coding=utf-8
import urllib2
import csv


def int_input(message):
    while True:
        try:
            number = int(raw_input("\n%s: " % message))
            return number
        except ValueError:
            print "\nPlease input an integer"
            continue


def main():
    print "\nThis program lets you make a table containing the most popular artists on Last.fm by chosen tag"
    musicians = []
    while True:
        tag = raw_input("\nChoose a tag: ").lower()
        if tag:
            break

    min_lis = int_input("Minimum number of listeners")
    max_art = int_input("Maximum number of top artists")

    print '\nLooking for artists with %s tag and minimum of %d listeners\n' % (tag, min_lis)
    print 'This might take a while...\n'

    for i in range(1, 50):
        address = 'http://www.last.fm/ru/tag/%s/artists?page=%s' % (tag, i)
        try:
            url = urllib2.urlopen(address)
        except urllib2.HTTPError:
            print "Page %s does not exist" % i
            break
        page = url.read()
        spage = page.split('\n')
        mus_count = 0
        for line in spage:
            if '/ru/music/' in line:
                string = spage[spage.index(line) + 5]
                number_string = spage[spage.index(line) + 13].strip()
                try:
                    name = string[string.index('>') + 1:string.index('<')].replace('&#39;', "'").replace('&amp;', '&')
                    listeners = int(number_string[0:number_string.index(' <span')].replace('\xc2\xa0', ''))
                    mus_count += 1
                    if not [name, listeners] in musicians and listeners >= min_lis:
                        musicians.append([name, listeners])
                except:
                    continue
        if mus_count == 0:
            print "There are only %s pages" % (i - 1)
            break

    if len(musicians) == 0:
        print "Sorry, we couldn't find anything\n"
        quit()

    musicians.sort(key=lambda x: x[1], reverse=True)

    file_name = 'musicians.csv'
    with open(file_name, 'w') as output:
        writer = csv.writer(output, lineterminator='\n')
        for m in range(max_art):
            if m > len(musicians) - 1:
                break
            writer.writerow(musicians[m])

    print "Done! Check the file musicians.csv\n"

main()
