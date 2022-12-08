Param(

    [Parameter(Mandatory,ValueFromPipeline,HelpMessage='Enter image name type = String)')]
    [Alias('image','image_name','in')]
    [string]
     $ImageName,

    [Parameter(Mandatory,ValueFromPipeline,HelpMessage='Enter container name (type = String)')]
    [Alias('container','container_name','cn')]
    [string]
     $ContainerName,

     [Parameter(Mandatory = $false,ValueFromPipeline=$false)]
     [Alias('run','start','st','rn')]
     [Switch]$gorun

) # On r�cup�re les param�tre

if($ImageName.Length -lt 3)
{
  $error = [string]"The image name length must be than or equal of 4"
  Write-Error -Message  $error -Category InvalidArgument
  return;
} # On check si la longueur de ImageName est < que 4

if($ContainerName.Length -lt 3)
{
  $error = [string]"The container name length must be than or equal of 4"
  Write-Error -Message  $error -Category InvalidArgument
  return;
  
} # On check si la longueur du ContainerName est < que 4

$env:ENV_IMAGE_NAME = $ImageName # l'image pour le docker-compose.yml
$env:ENV_CONTAINER_NAME = $ContainerName # le nom du containeur pour le docker-compose.yml

docker build . -t $ImageName

docker compose  -p $ContainerName  create --no-recreate # On monte le containeur

if($gorun.IsPresent)
{
   # cls
   docker start -a -i $ContainerName

} # Si on run ou pas (-run / -start)
