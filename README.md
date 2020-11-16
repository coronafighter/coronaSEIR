# coronavirus blood type (ABH, ABO, AB0) extended SEIR modeling and real world data correlation (experimental)

SEIR model based on: https://github.com/coronafighter/coronaSEIR  
  
ABH concept based on paper: Inhibition of the interaction between the SARS-CoV spike protein and its cellular receptor by anti-histo-blood group antibodies. https://www.ncbi.nlm.nih.gov/pubmed/18818423   (old SARS!)  
  
Reddit discussion: https://old.reddit.com/r/COVID19/comments/fjzjpc/relationship_between_the_abo_blood_group_and_the/fkpwxs6/
  
## ELI5 background
Most body cells are antigen marked similar like red blood cells with code A, B, AB or none (0, O, H; this is very simplified). Also some viruses that are created from body cells show these antigen tags on their surfaces. It has been suspected that our immune system can use these markings to quickly fight off viruses that show tags other than cells of the own body. E.g. a virus that was build in another persons body that has an incompatible blood type can be immediately destroyed because from the tag is clear that it does not belong here. On the other hand side this would mean that people of the same blood type (or compatible like A --> AB or 0 --> B) could more easily infect each other. Maybe the whole blood type system evolved because it slowed down the spread of infections.

## Findings
* There is no automatically 'best' or 'worst' blood type, it can depend on the relation of blood types in your society. See list below how your country would compare to others solely based on this model.
* The more 'diverse' the composition of blood types in a society the slower an epidemic would progress. E.g. if everybody had the same blood type it would be bad because there are no viruses with incompatible tags that can be detected easier.
* There seems to be a correlation of real world COVID-19 fatalities in countries compared to model predictions (see screenshot below).

## Open questions / ideas
* ABH: Is it possible to measure epidemic progression through blood type monitoring of cases? The proportion of blood types in cases should change over time to some extend.
* Is it more likely for type A to infect type A than for type 0 to infect type A? ("mimicry?") Simulation results in a slightly better match (factor 'd').

## See also
* Modelling suggests blood group incompatibility may substantially reduce SARS-CoV-2 transmission https://www.medrxiv.org/content/10.1101/2020.07.13.20152637v2

## Screenshots
![data](https://github.com/coronafighter/coronaSEIR/blob/master/screenshots/AB0.png)
![data](https://github.com/coronafighter/coronaSEIR/blob/ABH/screenshots/ABH_model_vs_world.png)

## How hard would my country be hit from a ABH model perspective 
```
                              Chile 100.0
                            Ecuador 96.0
                               Peru 93.4
                           Colombia 92.6
                          Venezuela 90.5
                           Zimbabwe 90.5
                        El Salvador 90.4
                           Honduras 89.6
                             Mexico 88.9
   Democratic Republic of the Congo 88.7
                            Bolivia 87.9
                            Iceland 87.9
                            Ireland 87.8
                              Ghana 87.7
                           Mongolia 87.7
                              Egypt 87.3
                             Russia 86.8
                          Argentina 86.5
                               Cuba 86.4
                          Australia 86.4
                        Netherlands 86.3
                   Papua New Guinea 86.3
                              Italy 86.1
                             Canada 86.0
                           Portugal 85.9
                            Nigeria 85.7
                             Norway 85.6
                              Yemen 85.6
                             Brazil 85.6
                              Spain 85.6
                     United Kingdom 85.6
                              Sudan 85.5
                        New Zealand 85.4
                      United States 85.3
                                 US 85.3
                       Saudi Arabia 85.3
                            Belgium 85.3
                              Libya 85.2
                            Lebanon 85.2
                            Bahrain 85.2
                             Uganda 85.1
                            Denmark 85.0
                             France 84.9
                            Jamaica 84.9
                 Dominican Republic 84.9
                         Mauritania 84.7
                              Syria 84.6
                           Cameroon 84.6
                            Germany 84.5
                          Luxemburg 84.5
                       South Africa 84.5
                             Greece 84.4
                             Guinea 84.4
                            Morocco 84.4
                           Cambodia 84.2
                              China 84.2
                        Ivory Coast 84.2
               United Arab Emirates 84.2
                          Lithuania 84.1
                              Kenya 83.9
                             Cyprus 83.8
                             Sweden 83.8
                               Fiji 83.4
                            Armenia 83.2
                          Singapore 82.9
                           Thailand 82.8
                             Serbia 82.8
                             Taiwan 82.8
                           Slovenia 82.6
             Bosnia and Herzegovina 82.6
                            Austria 82.5
                            Vietnam 82.3
                           Ethiopia 82.3
                          Macedonia 82.2
                            Ukraine 82.1
                              Macao 82.0
                          Hong Kong 82.0
                           Bulgaria 82.0
                             Turkey 81.8
                        Switzerland 81.8
                            Croatia 81.7
                            Romania 81.7
                          Mauritius 81.4
                            Finland 81.3
                             Israel 81.2
                             Latvia 81.2
                     Czech Republic 81.1
                              Korea 81.0
                        South Korea 81.0
                           Slovakia 81.0
                               Iran 80.9
                            Albania 80.8
                             Poland 80.8
                          Indonesia 80.8
                        Philippines 80.8
                            Myanmar 80.7
                            Hungary 80.7
                Republic of Moldova 80.7
                               Iraq 80.4
                              Nepal 80.3
                              Japan 80.3
                            Estonia 80.3
                         Bangladesh 80.1
                           Malaysia 80.0
                              India 79.8
                         Kazakhstan 79.7
                           Pakistan 79.3
```

## Credits
Country blood type data: http://www.rhesusnegative.net/themission/bloodtypefrequencies/  
also see master repository  
  
## License
MIT license
