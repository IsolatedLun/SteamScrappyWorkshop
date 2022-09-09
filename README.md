# SteamDownloader

Download or search any items/collections.

## Examples

- If you want to use the app's name eg. **rimworld** instead of it's id **294100**, then you have to add it to the aliases via `aliases --add 294100`
- So `search rimworld "Combat extended"` works instead of `search 294100 "Combat extended"`

<br />

Output :

```
1. Combat Extended - 1631756268
2. Combat Extended - 960196012
3. Combat Extended Guns - 1582570547
4. Combat Extended Melee - 1924933379
5. Combat Effects for Combat Extended - 1756442393
...
```

- You can either select all items by typing `all` or select multiple ones by `1 2 3` or `exit`
- For collections you cannot select multiple items, all of them will be added but you can remove an item using `items --remove INDEX`

<br />

- Outputting is simple, using `output` with use the **Output path** from `config.json`, you can change it from there **OR** just use `output --out_dir "MY FILE NAME.txt"`

## Dependencies

- You need [SteamCmd](https://developer.valvesoftware.com/wiki/SteamCMD#Downloading_SteamCMD) installed on your pc and specify it's location in `config.json`.

### How to use

- Clone this repo
- Tweak `config.json`
- `python main.py`

**No external python dependencies, all are built-in modules (I think)**

#### Misc

- If you want every output file to be unique and just create files in the root directory make `out_dir` -> `null`.

- If you want to output to your own specified folder open `config.json` and change `out_dir`.

#### Output Directory examples

**`out_dir` must always have a forward slash with closing braces `name_of_folder/{}`**

- `customFolder/{}` => `output`, Result: `customFolder/items-0-ABC.txt`
- `customFolder/{}/{}` => `output --dir customSubFolder *`, Result: `customFolder/customSubFolder/items-0-ABC[scrappyd].txt`
