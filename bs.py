from bs4 import BeautifulSoup

with open('Vocabulaire_2023_1_5.htm') as fp:
    soup = BeautifulSoup(fp, 'html.parser')

with open('send_to_anki.txt', 'w') as f:
    for div in soup.find_all('div', {'class': 'a9l-box-vocabulary'}):

        #if 'Verdammt' in str(div):
        if True:

            # download audio
            audios = div.find_all('div', {'class': 'pronunciation-players'})
            audio_src = []
            for audio in audios:
                audio_links = BeautifulSoup(audio.span['data-audio'], 'html.parser')
                audio_src.append(f"[sound:{audio_links.audio.source['src']}]")

            # get definitions
            conjug_table = ''
            words = div.find_all('p')
            for i, word in enumerate(words):
                for span in word.find_all('span', {'class': 'manual-trigger-request'}):
                    span.decompose()
                if i%2 == 1:
                    if word.find_next_sibling('span'):
                        conjug = None
                        if word.find_next_sibling('span')['class'][0] != 'wordkc-tags-label':
                            try:
                                conjug = BeautifulSoup(word.find_next_sibling('span')['data-content'], 'html.parser')
                            except (TypeError, KeyError) as e:
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
                            conjug_table = '\n'.join(conjug_table_list).strip()

                        #print('\n'.join(span.get_text() for span in conjug.div.next_sibling))

            #if len(words) % 2:
            #    if words[-1].find('span') is None:
            #    # has note
            #        print([p.contents for p in words])
            #        #print(div.find_all('p'))

            len_notes = len(words) - 2*len(audio_src)

            german = []
            for i in range(0, 2*len(audio_src), 2):
                german.append(words[i])
                try:
                    assert len(words[i].contents) == 1
                except AssertionError:
                    print('AssertionError:')
                    print(words[i], words[i].contents)
            german = '\n'.join([str(p.contents[0]) for p in german])

            english = []
            for i in range(1, 2*len(audio_src), 2):
                english.append(words[i])
            english = '\n'.join([str(p.contents[0]) for p in english])

            note = ''
            comments = []
            if len_notes:
                for p in words[2*len(audio_src):]:
                    for span in p.find_all('span', {'class': 'icon-tooltip a9tooltip'}):
                        comments.append(span['data-content'])
                        span.decompose()
                comments = ''.join(comments).strip()

                note = '\n'.join(
                    [' '.join([str(pp).strip() for pp in p.contents]) for p in words[2*len(audio_src):]]
                ).strip()
            if conjug_table:
                note = (conjug_table + '\n' + note).strip()
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
            print(note)
            print('-----------------')
            print(audio_src)
            print('------END--------')

            card = ';'.join([german.replace('\n', '<br />'), english.replace('\n', '<br />'), note.replace('\n', '<br />'), audio_src.replace('\n', '<br />')])
            f.write(card)
            f.write('\n')

