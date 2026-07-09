# Addin for existing nginx cconfiuration

Too add static version of the front to existing nginx configuration, use a
/etc/nginx/site-avaible + site-enable composition, like for the moode.audio example within
etc/nginx subdir.

This configration requires two distinct FQDNs for the host (in the example moode.lan. and
        kolekcje.lan.). Files altered

```bash
etc/nginx/kolekcje-locations.conf
etc/nginx/sites-available/kolekcje-http.conf
etc/nginx/sites-available/moode-http.conf
```

Do not forget link (symbolic) these files to `etc/nginx/sites-enabled/`.

