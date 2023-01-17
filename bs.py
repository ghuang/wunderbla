from bs4 import BeautifulSoup

#with open('Vocabulaire_2023_1_5.htm') as fp:
with open('Vocabulaire_2023_1_16.htm') as fp:
    soup = BeautifulSoup(fp, 'html.parser')

with open('send_to_anki.txt', 'w') as f:
    for div in soup.find_all('div', {'class': 'a9l-box-vocabulary'}):

        #if True:
        #if 'Prost' in str(div):
        if 'empfehle' in str(div):
        #if 'Wie geht es dir' in str(div):
        #if 'lecker' in str(div):
        #if 'evil' in str(div):
        #if 'Biegen Sie' in str(div):
        #if 'Sigi to help' in str(div):
        #if 'Kipferl' in str(div):

            # download audio
            audios = div.find_all('div', {'class': 'pronunciation-players'})
            audio_src = []
            for audio in audios:
                audio_links = BeautifulSoup(audio.span['data-audio'], 'html.parser')
                audio_src.append(f"[sound:{audio_links.audio.source['src']}]")

            # get labels
            labels = div.find_all('span', {'class': 'wordkc-tags-label'})
            if labels:
                labels = '\n'.join([span.get_text() for span in labels])
            else:
                labels = ''

            # get definitions
            conjug_table = []
            words = div.find_all('p')
            for i, word in enumerate(words):
                for span in word.find_all('span', {'class': 'manual-trigger-request'}):
                    span.decompose()

                if word.find_next_sibling('span'):
                    conjug = None
                    if word.find_next_sibling('span')['class'][0] != 'wordkc-tags-label':
                        try:
                            #conjug = BeautifulSoup(word.find_next_sibling('span')['data-content'], 'html.parser')
                            conjug = BeautifulSoup(word.find_next_sibling('span')['title'], 'html.parser')
                        except (TypeError, KeyError) as e:
                            print(word.find_next_sibling('span'))
                            raise e
                    if conjug and conjug.find('div', {'class': 'conjugation-grid-cells'}):
                        #print(conjug.div.get_text())
                        #print(conjug.get_text())
                        for span in conjug.find('div', {'class': 'conjugation-grid-cells'}).find_all('span'):
                            formats = span.find('span', {'class': 'correct'})
                            if formats:
                                formats.name = 'b'
                                del formats['class']
                        conjug_table_list = []
                        for span in conjug.find('div', {'class': 'conjugation-grid-cells'}).find_all('span'):
                            conjug_table_list.append(''.join([str(p) for p in span.contents]))
                        conjug_table.append('\n'.join(conjug_table_list).strip())

            if conjug_table:
                titles = div.find_all(class_='icon-tooltip conjugation-tooltip a9tooltip')
                if titles:
                    titles = [title.get_text() for title in titles]
                assert len(conjug_table) == len(titles)
                conjug_table  = '\n'.join([f'{a}\n{b}' for a, b in zip(titles, conjug_table)])
                #conjug_table = '\n'.join([titles, conjug_table])
                #print(conjug_table)


            #if conjug and conjug.find('div', {'class': ''}):
            #    print(conjug.find('div', {'class': 'icon-tooltip conjugation-tooltip a9tooltip'}).get_text())

            #if len(words) % 2:
            #    if words[-1].find('span') is None:
            #    # has note
            #        print([p.contents for p in words])
            #        #print(div.find_all('p'))

            german, english, comments = [], [], []
            for word in words:
                div = word.find_parent('div')
                if div['class'][0] == 'a9l-wordkc-parts':
                    if len(german) > len(english):
                        english.append(word)
                    else:
                        german.append(word)
                elif div['class'][0] == 'a9l-kc-text-lang' or div['class'][0] == 'a9t-kc-example':
                    comments.append(word)
            #print(german)
            #print(english)
            for comment in comments:
                print(comment)

            #len_notes = len(words) - 2*len(audio_src) if len(audio_src) else 0
            #try:
            #    assert len_notes == len(comments)
            #except AssertionError:
            #    print(comments)
            #    raise AssertionError

            #for i in range(0, 2*len(audio_src), 2):
            #for i in range(0, len(words), 2):
            #    if len(german) < 2*len(audio_src):
            #        german.append(words[i])
            #    try:
            #        assert len(words[i].contents) == 1
            #    except AssertionError:
            #        print('AssertionError:')
            #        print(words[i], words[i].contents)
            #        raise AssertionError
            #german = '\n'.join([str(p.contents[0]) for p in german])
            german = '\n'.join([' '.join([str(pp) for pp in p.contents]) for p in german])

            #english = []
            #for i in range(1, 2*len(audio_src), 2):
            #    english.append(words[i])
            english = '\n'.join([' '.join([str(pp) for pp in p.contents]) for p in english])

            note = ''
            #comments_in_str = ''
            #comments_in_str = []
            #if comments:
            ##    #for p in words[2*len(audio_src):]:
            #    for p in comments:
            #        if p.find('span', {'class': 'icon-tooltip a9tooltip'}):
            #            for span in p.find_all('span', {'class': 'icon-tooltip a9tooltip'}):
            #                #comments_in_str.append(span['data-content'])
            #                span.decompose()
            #                comments_in_str.append(p.contents[0])
            #                comments_in_str.append(span['title'])
            #        elif p.contents:
            #            comments_in_str.append(p.contents[0])
                #comments_in_str = ''.join(comments_in_str).strip()
            #comments = '\n'.join([' '.join([str(pp).strip() for pp in p.contents]) for p in comments])
            #comments = comments + comments_in_str
            #comments_in_str = ' '.join(comments_in_str).strip()
            #print(comments_in_str)

            for comment in comments:
                if comment.find('span', {'class': 'icon-tooltip a9tooltip'}):
                    for span in comment.find_all('span', {'class': 'icon-tooltip a9tooltip'}):
                        #popup_text = ' '.join([str(pp).strip() for pp in span.contents])
                        popup_text = ': '.join([span.contents[0], span['title']])
                        print(popup_text)
                        span.decompose()
                        #comment.insert(-1, popup_text)
                        comment.contents.append('<br>'+popup_text)

            #for comment in comments:
            #    print(comment)

            comments = '\n'.join([' '.join([str(pp).strip() for pp in p.contents]) for p in comments])

            #    note = '\n'.join(
            #        [' '.join([str(pp).strip() for pp in p.contents]) for p in words[2*len(audio_src):]]
            #    ).strip()
            if conjug_table:
                note = (conjug_table + '\n\n' + note).strip()
            if comments:
                note = (note + '\n\n' + comments).strip()

            if audio_src:
                audio_src = '\n'.join(audio_src)
            else:
                audio_src = ''

            print('-----BEGIN-------')
            print(german)
            print('-----------------')
            print(english)
            print('-----------------')
            print(labels)
            print('-----------------')
            print(note)
            print('-----------------')
            print(audio_src)
            print('------END--------')

            card = ';'.join([
                german.replace(';', ',').replace('\n', '<br />'), 
                labels.replace(';', ',').replace('\n', '<br />'), 
                note.replace(';', ',').replace('\n', '<br />'),
                english.replace(';', ',').replace('\n', '<br />'), 
                audio_src.replace('\n', '<br />')
            ])
            f.write(card)
            f.write('\n')

