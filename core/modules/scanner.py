import nmap
from core.modules.database import *
import typer
# Initialisation de l'outil nmap
nm = nmap.PortScanner()

# Fonction de scan des ports
def portScanner(ip: str, ports: str):
    try:
        # Lancer le scan
        nm.scan(ip, ports)
        
        # Vérification de l'état de l'hôte
        if ip in nm.all_hosts():
            host_info = nm[ip]  # Informations sur l'hôte
            if 'tcp' in host_info:
                # Liste des ports et informations associés
                port_info = {}
                for port in host_info['tcp']:
                    port_info[port] = {
                        'state': host_info['tcp'][port]['state'],
                        'name': host_info['tcp'][port].get('name', 'N/A'),
                        'product': host_info['tcp'][port].get('product', 'N/A'),
                        'version': host_info['tcp'][port].get('version', 'N/A'),
                    }
                return port_info
            else:
                return "Aucun port TCP trouvé."
        else:
            return f"L'hôte {ip} n'a pas pu être atteint."
    except Exception as e:
        return f"Erreur pendant le scan: {e}"
    


def osDetection(ip: str) -> dict:
    try:
        nm.scan(ip, arguments='-O')  # -O = OS detection
        if ip in nm.all_hosts() and 'osmatch' in nm[ip]:
            return {
                'os': nm[ip]['osmatch'][0]['name'] if nm[ip]['osmatch'] else "OS non détecté"
            }
        return { 'error': f"Aucune information sur l'OS pour {ip}" }
    except Exception as e:
        return { 'error': f"Erreur de détection d'OS : {e}" }


def osDetect(ip):
    result = osDetection(ip)
    init_db()
    addScannerOutput("osDetect", str(result))
    if isinstance(result, dict) and 'os' in result:
        typer.echo(f"\n🧠 Système d'exploitation détecté : {result['os']}")
    else:
        typer.secho(f"❌ OS non détecté ou erreur : {result}", fg=typer.colors.RED)