# Primary Object
<!-- All H1 tags will be ignored and H2 tags will be considered as the base object. H3 will be the internal k-v pair. -->

## Adding a file to Microsoft Windows Defender Exclusion List

> windows, defender, exclusion, add, file

### cmd

```powershell
Add-MpPreference -ExclusionPath <PATH>
```

### description

Powershell command to add exclusion

### examples

```powershell
Add-MpPreference -ExclusionPath C:\\Users\\user\\Desktop\\file.exe
```

## Adding a folder to Microsoft Windows Defender Exclusion List

> windows, defender, exclusion, add, folder

### cmd

```powershell
Add-MpPreference -ExclusionPath <PATH>
```

### description

Powershell command to add exclusion

### examples

```powershell
Add-MpPreference -ExclusionPath C:\\Users\\user\\Desktop\\folder
```
