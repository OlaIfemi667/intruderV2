from core.modules.scanner import *
from core.modules.database import *
import typer

from typing import Annotated

app = typer.Typer()

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
        

@app.command()
def osDetect(ip: Annotated[str, typer.Argument(help="IP address to scan OS")]):
    result = osDetection(ip)
    init_db()
    addScannerOutput("osDetect", str(result))
    if isinstance(result, dict) and 'os' in result:
        typer.echo(f"\n🧠 Système d'exploitation détecté : {result['os']}")
    else:
        typer.secho(f"❌ OS non détecté ou erreur : {result}", fg=typer.colors.RED)

        

if __name__ == "__main__":
    app()