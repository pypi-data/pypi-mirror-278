import argparse
import os
import pathlib
import random
import re

from PIL import Image
from audio2splitted.audio2splitted import split_audio
from dotenv import load_dotenv
from pytube.extract import video_id
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from mutagen.mp4 import MP4
from datetime import timedelta

from ytb2audio.ytb2audio import download_audio, download_thumbnail


def get_youtube_move_id(url: str):
    try:
        movie_id = video_id(url)
    except Exception as e:
        return None
    return movie_id


def output_filename_in_telegram(text):
    name = (re.sub(r'[^\w\s\-\_\(\)\[\]]', ' ', text)
                .replace('    ', ' ')
                .replace('   ', ' ')
                .replace('  ', ' ')
                .strip())

    return f'{name}.m4a'


DATA_DIR = 'data'


TIMECODES_THRESHOLD_COUNT = 3


def clean_timecodes_text(text):
    text = (text
            .replace('---', '')
            .replace('--', '')
            .replace('===', '')
            .replace('==', '')
            .replace(' =', '')
            .replace('___', '')
            .replace('__', '')
            .replace('_ _ _', '')
            .replace('_ _', '')
            .replace(' _', '')
            .replace('\n-', '')
            .replace('\n=', '')
            .replace('\n_', '')
            .replace('\n -', '')
            .replace('\n =', '')
            .replace('\n _', '')
            .strip()
            .lstrip()
            .rstrip()
            )
    return text


def get_timecodes_text(description):
    if not description:
        return
    if type(description) is not list:
        return
    if len(description) < 1:
        return ''

    for part in description[0].split('\n\n'):
        matches = re.compile(r'(\d{1,2}:\d{2})').findall(part)
        if len(matches) > TIMECODES_THRESHOLD_COUNT:
            return clean_timecodes_text(part)


def capital2lower_letters_filter(text):
    CAPITAL_LETTERS_PERCENT_THRESHOLD = 0.5
    count_capital = sum(1 for char in text if char.isupper())
    if count_capital / len(text) < CAPITAL_LETTERS_PERCENT_THRESHOLD:
        return text

    text = text.lower()
    text = text[0].upper() + text[1:]
    return text


def img_compress_and_resize(path: pathlib.Path, quality: int = 80, thumbnail_size = (960, 960)):
    image = Image.open(path)
    image.thumbnail(thumbnail_size)
    image.save(path, optimize=True, quality=quality)


async def processing_ytb2audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text:
        print('⛔️ No update.message.text. Skip.')
        return

    if not (movie_id := get_youtube_move_id(update.message.text)):
        print('⛔️ Not a Youtube Url. Skip.')
        return

    post_status = await context.bot.send_message(
        chat_id=update.message.from_user.id,
        reply_to_message_id=update.message.id,
        text=f'⌛️ Downloading ... '
    )

    audio = download_audio(movie_id, DATA_DIR)
    audio = pathlib.Path(audio)
    if not audio.exists():
        error_text = f'🟥 Unexpected error. After Check m4a_file.exists.'
        print(error_text)
        await post_status.edit_text(error_text)
        return

    thumbnail = download_thumbnail(movie_id, DATA_DIR)
    thumbnail = pathlib.Path(thumbnail)
    if not thumbnail.exists():
        error_text = f'🟥 Unexpected error. After Check thumbnail.exists().'
        print(error_text)
        await post_status.edit_text(error_text)
        return

    img_compress_and_resize(thumbnail)

    audios = split_audio(
        audio=audio,
        folder=pathlib.Path(DATA_DIR)
    )
    print('🟪 ', audios)

    await post_status.edit_text('⌛ Uploading to Telegram ... ')
    for idx, audio_part in enumerate(audios, start=1):
        path = audio_part.get('path')
        print('🔻', path)
        path = pathlib.Path(DATA_DIR).joinpath(path.name)
        print(path)
        try:
            m4a = MP4(path)
        except Exception as e:
            error_text = f'🟥 Exception as e: [m4a = MP4(m4a_file.as_posix())]. \n\n{e}'
            print(error_text)
            await post_status.edit_text(error_text)
            return

        if not m4a:
            error_text = '🟥 Unexpected error. [not audio in MP4 metadata].'
            print(error_text)
            await post_status.edit_text(error_text)
            return

        duration_seconds = None
        if m4a.info.length:
            duration_seconds = int(m4a.info.length)

        title = str(movie_id)
        if m4a.get('\xa9nam'):
            title = m4a.get('\xa9nam')[0]

        url_youtube = f'youtu.be/{movie_id}'
        link = f'<a href=\"{url_youtube}\">{url_youtube}</a>'

        title = capital2lower_letters_filter(title)

        meta_ver1 = f'{link} [{timedelta(seconds=duration_seconds)}]'
        meta_ver2 = f'[{timedelta(seconds=duration_seconds)}] {link}'
        meta_info = random.choice([meta_ver1, meta_ver2])

        caption = f'{title}\n{meta_info}'
        filename = output_filename_in_telegram(title)

        timecodes = get_timecodes_text(m4a.get('desc'))
        if timecodes:
            caption = f'{caption}\n\n{timecodes}'

        if len(audios) > 1:
            filename = f'(p{idx}-of{len(audios)}) {filename}'
            caption = f'[Part {idx} of {len(audios)}] {caption}'

        with thumbnail.open('rb') as thumbnail_file:
            await context.bot.send_audio(
                chat_id=update.message.from_user.id,
                reply_to_message_id=None if idx > 1 else update.message.id,
                audio=audio.as_posix(),
                duration=duration_seconds,
                filename=filename,
                thumbnail=thumbnail_file,
                caption=caption,
                parse_mode=ParseMode.HTML
            )
    await post_status.delete()

    if context.bot_data.get('keepfiles') == 0:
        for file in filter(lambda f: f.name.startswith(movie_id), pathlib.Path(DATA_DIR).iterdir()):
            try:
                file.unlink()
            except Exception as e:
                print(f'🟠 Failed to delete {file}: {e}')

    print(f'💚 Success! [{movie_id}]\n')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Help text',
        parse_mode=ParseMode.HTML
    )


def run_bot(token: str, opt_keepfiles: str):
    print('🚀 Run bot...')

    application = ApplicationBuilder().token(token).build()

    application.bot_data['keepfiles'] = opt_keepfiles

    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, processing_ytb2audio))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    parser = argparse.ArgumentParser(description='Bot ytb 2 audio')
    parser.add_argument('--keepfiles', type=int,
                        help='Keep raw files 1=True, 0=False (default)', default=0)

    args = parser.parse_args()

    load_dotenv()
    token = os.environ.get("TG_TOKEN")
    if not token:
        print('⛔️ No telegram bot token. Exit')
        return

    run_bot(token, args.keepfiles)


if __name__ == "__main__":
    main()
