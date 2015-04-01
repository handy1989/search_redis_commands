grep -n "<li data-group" Redis_cmd.html | grep data-group | sed  's/.*data-group=\([^>]*\)*>.*href=\([^>]*\)>\([^<]*\)<.*&nbsp;\([^<]*\)<.*class="summary">\([^<]*\).*/\1 # \2 # \3#\4 # \5/g'
