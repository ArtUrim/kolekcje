<!DOCTYPE html>
<html lang="pl" dir="ltr">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="robots" content="noindex">
<title>Eksport: katalog - db - Adminer</title>
<link rel="stylesheet" type="text/css" href="?file=default.css&amp;version=4.8.1">
<script src='?file=functions.js&amp;version=4.8.1' nonce="MTAxYjkwZDFkOTIxZGVmOWRjYTU1ZGQyZDE2NjdhZDk="></script>
<link rel="shortcut icon" type="image/x-icon" href="?file=favicon.ico&amp;version=4.8.1">
<link rel="apple-touch-icon" href="?file=favicon.ico&amp;version=4.8.1">

<body class="ltr nojs">
<script nonce="MTAxYjkwZDFkOTIxZGVmOWRjYTU1ZGQyZDE2NjdhZDk=">
mixin(document.body, {onkeydown: bodyKeydown, onclick: bodyClick});
document.body.className = document.body.className.replace(/ nojs/, ' js');
var offlineMessage = 'Jesteś offline.';
var thousandsSeparator = ' ';
</script>

<div id="help" class="jush-sql jsonly hidden"></div>
<script nonce="MTAxYjkwZDFkOTIxZGVmOWRjYTU1ZGQyZDE2NjdhZDk=">mixin(qs('#help'), {onmouseover: function () { helpOpen = 1; }, onmouseout: helpMouseout});</script>

<div id="content">
<p id="breadcrumb"><a href="?server=db">MySQL</a> &raquo; <a href='?server=db&amp;username=example' accesskey='1' title='Alt+Shift+1'>db</a> &raquo; <a href="?server=db&amp;username=example&amp;db=katalog">katalog</a> &raquo; Eksport
<h2>Eksport: katalog</h2>
<div id='ajaxstatus' class='jsonly hidden'></div>

<form action="" method="post">
<table cellspacing="0" class="layout">
<tr><th>Rezultat<td><label><input type='radio' name='output' value='text' checked>otwórz</label><label><input type='radio' name='output' value='file'>zapisz</label><label><input type='radio' name='output' value='gz'>gzip</label>
<tr><th>Format<td><label><input type='radio' name='format' value='sql' checked>SQL</label><label><input type='radio' name='format' value='csv'>CSV,</label><label><input type='radio' name='format' value='csv;'>CSV;</label><label><input type='radio' name='format' value='tsv'>TSV</label>
<tr><th>Baza danych<td><select name='db_style'><option selected><option>USE<option>DROP+CREATE<option>CREATE</select><label><input type='checkbox' name='routines' value='1' checked>Procedury i funkcje</label><label><input type='checkbox' name='events' value='1' checked>Wydarzenia</label><tr><th>Tabele<td><select name='table_style'><option><option selected>DROP+CREATE<option>CREATE</select><label><input type='checkbox' name='auto_increment' value='1'>Auto Increment</label><label><input type='checkbox' name='triggers' value='1' checked>Wyzwalacze</label><tr><th>Dane<td><select name='data_style'><option><option>TRUNCATE+INSERT<option selected>INSERT<option>INSERT+UPDATE</select></table>
<p><input type="submit" value="Eksport">
<input type="hidden" name="token" value="614308:268943">

<table cellspacing="0">
<script nonce="MTAxYjkwZDFkOTIxZGVmOWRjYTU1ZGQyZDE2NjdhZDk=">qsl('table').onclick = dumpClick;</script>
<thead><tr><th style='text-align: left;'><label class='block'><input type='checkbox' id='check-tables' checked>Tabele</label><script nonce="MTAxYjkwZDFkOTIxZGVmOWRjYTU1ZGQyZDE2NjdhZDk=">qs('#check-tables').onclick = partial(formCheck, /^tables\[/);</script><th style='text-align: right;'><label class='block'>Dane<input type='checkbox' id='check-data' checked></label><script nonce="MTAxYjkwZDFkOTIxZGVmOWRjYTU1ZGQyZDE2NjdhZDk=">qs('#check-data').onclick = partial(formCheck, /^data\[/);</script></thead>
<tr><td><label class='block'><input type='checkbox' name='tables[]' value='Authors' checked>Authors</label><td align='right'><label class='block'><span id='Rows-Authors'></span><input type='checkbox' name='data[]' value='Authors' checked></label>
<tr><td><label class='block'><input type='checkbox' name='tables[]' value='bookAuthors' checked>bookAuthors</label><td align='right'><label class='block'><span id='Rows-bookAuthors'></span><input type='checkbox' name='data[]' value='bookAuthors' checked></label>
<tr><td><label class='block'><input type='checkbox' name='tables[]' value='bookGenres' checked>bookGenres</label><td align='right'><label class='block'><span id='Rows-bookGenres'></span><input type='checkbox' name='data[]' value='bookGenres' checked></label>
<tr><td><label class='block'><input type='checkbox' name='tables[]' value='Books' checked>Books</label><td align='right'><label class='block'><span id='Rows-Books'></span><input type='checkbox' name='data[]' value='Books' checked></label>
<tr><td><label class='block'><input type='checkbox' name='tables[]' value='genres' checked>genres</label><td align='right'><label class='block'><span id='Rows-genres'></span><input type='checkbox' name='data[]' value='genres' checked></label>
<tr><td><label class='block'><input type='checkbox' name='tables[]' value='language' checked>language</label><td align='right'><label class='block'><span id='Rows-language'></span><input type='checkbox' name='data[]' value='language' checked></label>
<tr><td><label class='block'><input type='checkbox' name='tables[]' value='publisher' checked>publisher</label><td align='right'><label class='block'><span id='Rows-publisher'></span><input type='checkbox' name='data[]' value='publisher' checked></label>
<tr><td><label class='block'><input type='checkbox' name='tables[]' value='series' checked>series</label><td align='right'><label class='block'><span id='Rows-series'></span><input type='checkbox' name='data[]' value='series' checked></label>
<script nonce="MTAxYjkwZDFkOTIxZGVmOWRjYTU1ZGQyZDE2NjdhZDk=">ajaxSetHtml('?server=db&username=example&db=katalog&script=db');</script>
</table>
</form>
</div>

<form action='' method='post'>
<div id='lang'>Język: <select name='lang'><option value="en">English<option value="ar">العربية<option value="bg">Български<option value="bn">বাংলা<option value="bs">Bosanski<option value="ca">Català<option value="cs">Čeština<option value="da">Dansk<option value="de">Deutsch<option value="el">Ελληνικά<option value="es">Español<option value="et">Eesti<option value="fa">فارسی<option value="fi">Suomi<option value="fr">Français<option value="gl">Galego<option value="he">עברית<option value="hu">Magyar<option value="id">Bahasa Indonesia<option value="it">Italiano<option value="ja">日本語<option value="ka">ქართული<option value="ko">한국어<option value="lt">Lietuvių<option value="ms">Bahasa Melayu<option value="nl">Nederlands<option value="no">Norsk<option value="pl" selected>Polski<option value="pt">Português<option value="pt-br">Português (Brazil)<option value="ro">Limba Română<option value="ru">Русский<option value="sk">Slovenčina<option value="sl">Slovenski<option value="sr">Српски<option value="sv">Svenska<option value="ta">த‌மிழ்<option value="th">ภาษาไทย<option value="tr">Türkçe<option value="uk">Українська<option value="vi">Tiếng Việt<option value="zh">简体中文<option value="zh-tw">繁體中文</select><script nonce="MTAxYjkwZDFkOTIxZGVmOWRjYTU1ZGQyZDE2NjdhZDk=">qsl('select').onchange = function () { this.form.submit(); };</script> <input type='submit' value='Wybierz' class='hidden'>
<input type='hidden' name='token' value='414530:726633'>
</div>
</form>
<form action="" method="post">
<p class="logout">
<input type="submit" name="logout" value="Wyloguj" id="logout">
<input type="hidden" name="token" value="614308:268943">
</p>
</form>
<div id="menu">
<h1>
<a href='https://www.adminer.org/' target="_blank" rel="noreferrer noopener" id='h1'>Adminer</a> <span class="version">4.8.1</span>
<a href="https://www.adminer.org/#download" target="_blank" rel="noreferrer noopener" id="version"></a>
</h1>
<script src='?file=jush.js&amp;version=4.8.1' nonce="MTAxYjkwZDFkOTIxZGVmOWRjYTU1ZGQyZDE2NjdhZDk="></script>
<script nonce="MTAxYjkwZDFkOTIxZGVmOWRjYTU1ZGQyZDE2NjdhZDk=">
var jushLinks = { sql: [ '?server=db&username=example&db=katalog&table=$&', /\b(Authors|bookAuthors|bookGenres|Books|genres|language|publisher|series)\b/g ] };
jushLinks.bac = jushLinks.sql;
jushLinks.bra = jushLinks.sql;
jushLinks.sqlite_quo = jushLinks.sql;
jushLinks.mssql_bra = jushLinks.sql;
bodyLoad('11', true);
</script>
<form action="">
<p id="dbs">
<input type="hidden" name="server" value="db"><input type="hidden" name="username" value="example"><span title='baza danych'>DB</span>: <select name='db'><option value=""><option>information_schema<option selected>katalog</select><script nonce="MTAxYjkwZDFkOTIxZGVmOWRjYTU1ZGQyZDE2NjdhZDk=">mixin(qsl('select'), {onmousedown: dbMouseDown, onchange: dbChange});</script>
<input type='submit' value='Wybierz' class='hidden'>
<input type='hidden' name='dump' value=''></p></form>
<p class='links'><a href='?server=db&amp;username=example&amp;db=katalog&amp;sql='>Zapytanie SQL</a>
<a href='?server=db&amp;username=example&amp;db=katalog&amp;import='>Import</a>
<a href='?server=db&amp;username=example&amp;db=katalog&amp;dump=' id='dump' class='active '>Eksport</a>
<a href="?server=db&amp;username=example&amp;db=katalog&amp;create=">Utwórz tabelę</a>
<ul id='tables'><script nonce="MTAxYjkwZDFkOTIxZGVmOWRjYTU1ZGQyZDE2NjdhZDk=">mixin(qs('#tables'), {onmouseover: menuOver, onmouseout: menuOut});</script>
<li><a href="?server=db&amp;username=example&amp;db=katalog&amp;select=Authors" class='select' title='Pokaż dane'>przeglądaj</a> <a href="?server=db&amp;username=example&amp;db=katalog&amp;table=Authors" class='structure' title='Struktura tabeli'>Authors</a>
<li><a href="?server=db&amp;username=example&amp;db=katalog&amp;select=bookAuthors" class='select' title='Pokaż dane'>przeglądaj</a> <a href="?server=db&amp;username=example&amp;db=katalog&amp;table=bookAuthors" class='structure' title='Struktura tabeli'>bookAuthors</a>
<li><a href="?server=db&amp;username=example&amp;db=katalog&amp;select=bookGenres" class='select' title='Pokaż dane'>przeglądaj</a> <a href="?server=db&amp;username=example&amp;db=katalog&amp;table=bookGenres" class='structure' title='Struktura tabeli'>bookGenres</a>
<li><a href="?server=db&amp;username=example&amp;db=katalog&amp;select=Books" class='select' title='Pokaż dane'>przeglądaj</a> <a href="?server=db&amp;username=example&amp;db=katalog&amp;table=Books" class='structure' title='Struktura tabeli'>Books</a>
<li><a href="?server=db&amp;username=example&amp;db=katalog&amp;select=genres" class='select' title='Pokaż dane'>przeglądaj</a> <a href="?server=db&amp;username=example&amp;db=katalog&amp;table=genres" class='structure' title='Struktura tabeli'>genres</a>
<li><a href="?server=db&amp;username=example&amp;db=katalog&amp;select=language" class='select' title='Pokaż dane'>przeglądaj</a> <a href="?server=db&amp;username=example&amp;db=katalog&amp;table=language" class='structure' title='Struktura tabeli'>language</a>
<li><a href="?server=db&amp;username=example&amp;db=katalog&amp;select=publisher" class='select' title='Pokaż dane'>przeglądaj</a> <a href="?server=db&amp;username=example&amp;db=katalog&amp;table=publisher" class='structure' title='Struktura tabeli'>publisher</a>
<li><a href="?server=db&amp;username=example&amp;db=katalog&amp;select=series" class='select' title='Pokaż dane'>przeglądaj</a> <a href="?server=db&amp;username=example&amp;db=katalog&amp;table=series" class='structure' title='Struktura tabeli'>series</a>
</ul>
</div>
<script nonce="MTAxYjkwZDFkOTIxZGVmOWRjYTU1ZGQyZDE2NjdhZDk=">setupSubmitHighlight(document);</script>
