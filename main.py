from table_manager import TableManager
import json


def main():
    # Initialisierung des TableManager
    manager = TableManager()

    # Die Tabellen-ID für die Abfrage
    table_id = "table_01J7E85DYEXJNP6J6ZDWR1Q2F1ja"

    # Spalten abfragen - Erster Durchlauf
    print("Erster Durchlauf: Abfrage der Spalten:")
    columns = manager.get_table_columns(table_id)

    if columns:
        print("Spalten gefunden:", columns)
        print("\nNotiere dir die Spaltennamen, um im zweiten Durchlauf eine neue Zeile hinzuzufügen.")
    else:
        print("Keine Spalten gefunden oder ein Fehler ist aufgetreten.")
        return  # Beende das Programm, falls keine Spalten gefunden wurden

    # Zweiter Durchlauf: Eingabe für neue Zeile
    proceed = input("\nMöchtest du jetzt eine neue Zeile hinzufügen? (ja/nein): ").lower()
    if proceed != 'ja':
        print("Programm beendet.")
        return

    # Beispiel für den neuen Datensatz basierend auf den abgerufenen Spalten
    new_row_data = {}
    for column in columns:  # Gehe jede Spalte durch und frage den Benutzer nach Werten
        if column in ['id', 'createdAt', 'updatedAt', 'computed', 'stale']:  # Diese Felder werden vom System verwaltet
            continue
        value = input(f"Gib einen Wert für die Spalte '{column}' ein: ")
        new_row_data[column] = value

    print(f"\nHinzufügen der neuen Zeile mit den Daten: {new_row_data}")
    result = manager.add_row(table_id, new_row_data)

    if result:
        print(f"Zeile erfolgreich hinzugefügt:", json.dumps(result, indent=4))
    else:
        print(f"Fehler beim Hinzufügen der Zeile.")


if __name__ == "__main__":
    main()
