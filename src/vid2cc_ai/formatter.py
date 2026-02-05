def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    msecs = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{msecs:03}"

def save_as_srt(segments, output_path, max_chars=80):
    """
    Saves segments to SRT using word-level timestamps.
    max_chars=80 allows full sentences to fit on one line.
    """
    
    # Flatten all words if available
    all_words = []
    for seg in segments:
        if 'words' in seg:
            all_words.extend(seg['words'])
    
    # If no word timestamps (fallback), use original coarse segments
    if not all_words:
        with open(output_path, "w", encoding="utf-8") as f:
            for i, segment in enumerate(segments, start=1):
                start = format_timestamp(segment['start'])
                end = format_timestamp(segment['end'])
                f.write(f"{i}\n{start} --> {end}\n{segment['text'].strip()}\n\n")
        return

    subtitles = []
    current_line = []
    current_length = 0
    
    for i, word_data in enumerate(all_words):
        word = word_data['word'].strip()
        start = word_data['start']
        end = word_data['end']
        
        # Calculate visual length (+1 for the space)
        added_length = len(word) + 1 if current_length > 0 else len(word)
        
        # Check for significant pauses (> 1.0s) to force a new sentence
        long_pause = False
        if i > 0:
            prev_end = all_words[i-1]['end']
            if start - prev_end > 1.0:
                long_pause = True
        
        # Check for punctuation-based split
        # If the PREVIOUS word ended with punctuation and we have enough content -> split.
        sentence_break = False
        if current_line:
            last_word_char = current_line[-1]['word'].strip()[-1]
            if last_word_char in ['.', '!', '?'] and current_length > 20:
                sentence_break = True

        if (current_length + added_length > max_chars) or long_pause or sentence_break:
            # Finalize current line
            if current_line:
                subtitles.append({
                    "start": current_line[0]['start'],
                    "end": current_line[-1]['end'],
                    "text": " ".join([w['word'].strip() for w in current_line])
                })
            # Reset for new line
            current_line = [word_data]
            current_length = len(word)
        else:
            # Add to current line
            current_line.append(word_data)
            current_length += added_length

    if current_line:
        subtitles.append({
            "start": current_line[0]['start'],
            "end": current_line[-1]['end'],
            "text": " ".join([w['word'].strip() for w in current_line])
        })

    with open(output_path, "w", encoding="utf-8") as f:
        for i, sub in enumerate(subtitles, start=1):
            start_ts = format_timestamp(sub['start'])
            end_ts = format_timestamp(sub['end'])
            f.write(f"{i}\n{start_ts} --> {end_ts}\n{sub['text']}\n\n")