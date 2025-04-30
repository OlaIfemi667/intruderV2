from core.modules.scanner import *
from core.modules.database import *
from sublister.sublist3r import *
import typer
from subprocessUtils.subprocess import *

from typing import Annotated

app = typer.Typer()


#command for netword reconnaissance it is basically a nmap showing, service, version, ports and OS type

@app.command()
def netRecon(ip: Annotated[str, typer.Argument(help="IP address to scan")], ports: Annotated[str, typer.Option(help="Ports to scan (default is 22-80")] = "22-80"):
    result = portScanner(ip, ports)
    init_db()
    addScannerOutput("netRecon", str(result))
    if isinstance(result, dict):
        typer.echo("\n🔍 Résultats du scan :\n")
        for port, details in result.items():
            typer.echo(f"📌 Port {port} => {details['state'].upper()}")
            typer.echo(f"    └── Service : {details['name']}")
            typer.echo(f"    └── Produit : {details['product']}")
            typer.echo(f"    └── Version : {details['version']}\n")
    else:
        typer.secho(result, fg=typer.colors.RED)
    
    osDetect(ip)
        

#find subdomains for a domain 

@app.command()
def sublister( domain: Annotated[str, typer.Argument(help="domains to scan to scan OS")]):
    #Ici j'ai utiliser la function main de sublister que j'ai bebaptisé sublisterMain pour eviter les conflits.
    passsubdomains = sublisterMain(domain, 40, f"text/{domain}.txt", ports= None, silent=False, verbose= False, enable_bruteforce= False, engines=None)

@app.command()
def webfuzzer(url: Annotated[str, typer.Argument(help="an url")]):
    if not is_valid_url(url):
        print("❌ URL invalide. Utilise un format comme http://example.com")
        raise typer.Exit(code=1)

    domain = urlparse(url).netloc  # extrait le domaine
    asyncio.run(runCommand(f"nikto -h {domain}"))

if __name__ == "__main__":
    app()