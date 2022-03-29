using System;
using System.Collections.Generic;
using System.Linq;

// ReSharper disable PossibleNullReferenceException

// ReSharper disable LoopCanBeConvertedToQuery

namespace UTRLAB1
{
    /*Enka - epsilon nedeterministi?ki kona?ni automat. Polja _stanja, _abeceda i _prihvStanja se
    ne koriste pa su zakomentirana. Konstruktor ih prima kao agrumente ali polja ne postoje jer
    se ne koriste, a za slu?aj da nekad zatrebaju samo treba odkomentirati linije koje deklariraju
    te ?lanske varijable kao i linije koje ih u konstruktoru inicijaliziraju.*/
    internal class Enka
    {
        private List<string> _ulazniNiz;
        private HashSet<string> _trenutnaStanja;
        private readonly Dictionary<string, List<string>> _regularniPrijelazi;
        private Dictionary<string, List<string>> _epsilonPrijelazi;
        private HashSet<string> _stanjaSEpsilonPrijelazom;

        private int _duljinaUlaznogNiza;
        // private List<string> _stanja;
        // private List<string> _abeceda;
        // private List<string> _prihvStanja;

        /*Konstruktor prima sve podatke koje dobijemo u datoteci ali ne inicijalizira polja koja se ne koriste
        - obja?njeno u komentaru na po?etku, odmah prije deklariranja klase. Poziva i funkciju
        NapraviEpsilonPrijelaze(); budu?i da se oni doga?aju instantno, za slu?aj da iz po?etnog stanja postoje
        epsilon prijelazi.*/
        public Enka(List<string> ulazniNiz, List<string> stanja, List<string> abeceda, List<string> prihvStanja,
            HashSet<string> trenutnaStanja, Dictionary<string, List<string>> delta)
        {
            _ulazniNiz = ulazniNiz;
            _trenutnaStanja = trenutnaStanja;
            _regularniPrijelazi = delta;
            _duljinaUlaznogNiza = ulazniNiz.Count;
            foreach (var key in _regularniPrijelazi.Keys.ToList().Where(key => _regularniPrijelazi[key].Count == 1 && _regularniPrijelazi[key][0] == "#"))
            {
                _regularniPrijelazi.Remove(key);
            }
            _epsilonPrijelazi = new Dictionary<string, List<string>>();

            foreach (var key in _regularniPrijelazi.Keys.ToList())
            {
                if (key.EndsWith("$"))
                {
                    _epsilonPrijelazi.Add(key.Substring(0, key.Length - 2), delta[key]);
                    _regularniPrijelazi.Remove(key);
                }
            }
            _stanjaSEpsilonPrijelazom = new HashSet<string>();
            _stanjaSEpsilonPrijelazom.UnionWith(_epsilonPrijelazi.Keys.ToHashSet());
            NapraviEpsilonPrijelaze();
        }

        // Setter za ulazni niz - postavlja ulazni niz i ponovno izra?unava varijablu _duljinaUlaznogNiza.
        public void SetUlazniNiz(List<string> ulazniNiz)
        {
            _ulazniNiz = ulazniNiz;
            _duljinaUlaznogNiza = ulazniNiz.Count;
        }

        // Setter za _trenutnaStanja
        public void SetTrenutnaStanja(HashSet<string> trenutnaStanja)
        {
            _trenutnaStanja = trenutnaStanja;
        }

        // TODO add comment/docs here, optimized function
        private void NapraviEpsilonPrijelaze()
        {
            var novoDodanaStanja = new HashSet<string>();
            foreach (var stanje in _trenutnaStanja.ToList()) // TODO ovo mora? postati neki while, neces dodavati epsilon put nego prijelaz
            {
                if (_stanjaSEpsilonPrijelazom.Contains(stanje))
                {
                    if (_epsilonPrijelazi[stanje].Except(_trenutnaStanja).Any())
                    {
                        novoDodanaStanja.UnionWith(_epsilonPrijelazi[stanje].ToHashSet());
                        _trenutnaStanja.UnionWith(_epsilonPrijelazi[stanje]);
                    }
                }
            }
            while (novoDodanaStanja.Count() != 0)
            {
                foreach (var stanje in new List<string>(novoDodanaStanja))
                {
                    if (_stanjaSEpsilonPrijelazom.Contains(stanje) && _epsilonPrijelazi[stanje].Except(_trenutnaStanja).Any())
                    {
                        _trenutnaStanja.UnionWith(_epsilonPrijelazi[stanje]);
                        novoDodanaStanja.UnionWith(_epsilonPrijelazi[stanje]);
                    }
                    novoDodanaStanja.Remove(stanje);
                }
            }
        }


        /*Ne vra?a ni?ta - jednostavno pomi?e automat jedan korak unaprijed ?itaju?i sljede?i znak i
        primjenjuju?i prijelaze. Nakon prijelaza pozove metodu NapraviEpsilonPrijelaze(); budu?i da
        ?e stanja u koja prelazimo tim epsilon prijelazima pripadaju skupu trenutnih stanja istog koraka kao i 
        ova u koja smo do?li obi?nim, ne-epsilon prijelazima. Ako je ulazni niz prazan, vra?a se
        ne ?ine?i ni?ta - ovaj automat je gotov i nema vi?e promjena stanja. To je omogu?eno ?injenicom da se
        znakovi ulaznog niza nakon ?to se ?itaju odmah i obri?u, odnosno nulti se ?lan ?ita - bri?e - ?ita - bri?e,
        sve dok ne ponestane ulaznih znakova.*/
        private void NapraviPrijelaz()
        {
            if (_ulazniNiz.Count == 0)
            {
                return;
            }

            var stanjaUKojaDolazimo = new HashSet<string>();
            foreach (var stanje in _trenutnaStanja)
            {
                var trazenoStanjeIPrijelaz = stanje + "," + _ulazniNiz[0];
                if (_regularniPrijelazi.Keys.Contains(trazenoStanjeIPrijelaz))
                {
                    foreach (var novoStanje in _regularniPrijelazi[trazenoStanjeIPrijelaz])
                    {
                        stanjaUKojaDolazimo.Add(novoStanje);
                    }
                }
            }

            _trenutnaStanja.Clear();
            _trenutnaStanja.UnionWith(stanjaUKojaDolazimo);
            stanjaUKojaDolazimo.Clear();
            _ulazniNiz.RemoveAt(0);
            NapraviEpsilonPrijelaze();
        }

        // Vra?a string: trenutna stanja automata u leksikografskom poretku odvojena zarezom. '#' za prazan skup.
        private string GetStringTrenutnaStanja()
        {
            if (_trenutnaStanja.Count == 0)
            {
                return "#";
            }

            var trenutnaStanjaSortirana = _trenutnaStanja.ToList();
            trenutnaStanjaSortirana.Sort();

            var retVal = "";
            foreach (var stanje in trenutnaStanjaSortirana)
            {
                retVal += stanje + ",";
            }

            return retVal.Substring(0, retVal.Length - 1);
        }

        // Pokre?e automat, ispisuju?i stanja u koracima.
        public void PokreniAutomat()
        {
            NapraviEpsilonPrijelaze();
            Console.Write(GetStringTrenutnaStanja());
            for (var i = 0; i < _duljinaUlaznogNiza; i++)
            {
                NapraviPrijelaz();
                Console.Write("|" + GetStringTrenutnaStanja());
            }

            Console.WriteLine();
        }
    }

    internal static class Program
    {
        public static void Main(string[] args)
        {
            /*U?itavanje podataka iz stdin*/
            var ulazniNizovi = new List<List<string>>();
            foreach (var s in Console.ReadLine().Split('|'))
            {
                ulazniNizovi.Add(s.Split(',').ToList());
            }

            var stanja = Console.ReadLine().Split(',').ToList();
            var abeceda = Console.ReadLine().Split(',').ToList();
            var prihvStanja = Console.ReadLine().Split(',').ToList();
            var pocetnaStanja = new HashSet<string> { Console.ReadLine() };
            var delta = new Dictionary<string, List<string>>();
            var x = Console.Read();
            while (x != -1)
            {
                // ?ita dok postoji sljede?i character u stdin
                var linija = Console.ReadLine().Split('-');
                delta.Add((char)x + linija[0], linija[1].Substring(1).Split(',').ToList());
                x = Console.Read();
            }

            /* Stvaranje objekta tipa Enka */
            /* Koristim isti objekt automat za svaki ulazni niz, ali moram mu resetirati polja ulazniNiz i trenutnaStanja */
            var automat = new Enka(ulazniNizovi[0], stanja, abeceda, prihvStanja, new HashSet<string>(pocetnaStanja),
                delta);
            // Za svaki ulazni niz pokre?em automat

            //testing purposes, exiting here.
            //return;
            foreach (var ulazniNiz in ulazniNizovi)
            {
                automat.SetUlazniNiz(ulazniNiz);
                automat.SetTrenutnaStanja(new HashSet<string>(pocetnaStanja));
                automat.PokreniAutomat();
            }
        }
    }
}
