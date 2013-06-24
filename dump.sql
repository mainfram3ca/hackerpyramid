-- MySQL dump 10.13  Distrib 5.1.69, for unknown-linux-gnu (x86_64)
--
-- Host: localhost    Database: coolacid_10k
-- ------------------------------------------------------
-- Server version	5.1.69-cll

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `catagories`
--

DROP TABLE IF EXISTS `catagories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catagories` (
  `cat_id` int(2) DEFAULT NULL,
  `name` varchar(34) DEFAULT NULL,
  `hint` varchar(53) DEFAULT NULL,
  `celeb` varchar(15) DEFAULT NULL,
  `answers` varchar(185) DEFAULT NULL,
  `active` int(11) NOT NULL,
  `used` int(1) DEFAULT NULL,
  `next` int(1) DEFAULT NULL,
  `classic` int(1) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catagories`
--

LOCK TABLES `catagories` WRITE;
/*!40000 ALTER TABLE `catagories` DISABLE KEYS */;
INSERT INTO `catagories` VALUES (1,'Periodically','Rhymes with Pentium',NULL,',Titanium,Aluminium,Calcium,Helium,Platinum,Magnesium,Lithium',0,0,0,0),(2,'Hacker Kryptonite',NULL,NULL,',Sunlight,Exercise,DMCA,DRM,Management,The Feds,Decaffeinated Coffee',0,1,0,0),(3,'Authors',NULL,NULL,',Stephen King,George Orwell,Steven Levy,Clifford Stoll,Douglas Adams,Cory Doctorow,Douglas Coupland',0,0,0,0),(4,'Sci-Fi Grand Masters',NULL,NULL,',Isaac Asimov,Robert Heinlein,Frank Herbert,Orson Welles,Arthur C. Clarke,H. G. Wells,Jules Verne',0,0,0,0),(5,'Cyberpunk Authors',NULL,NULL,',William Gibson,Neal Stephenson,Bruce Bethke,Philip K. Dick,Bruce Sterling,Michael Swanwick,Rudy Rucker/Rudolf von Bitter Rucker',0,1,0,0),(6,'Short Circuits','From the Movie(s)',NULL,',Johnny 5,lightning bolt,Nova Laboratories ,Input,Malfunction,dissassemble,KIDNAP THE HUMANS!  DESTROY THE MACHINE!',0,0,0,0),(7,'Back to the Futures',NULL,NULL,',1.21 Gigawatts,88 MPH,Marty McFly,Libyans,Emmett Brown,Einstein,Jules & Verne',0,1,0,0),(8,'Notable H4X0RZ',NULL,NULL,',Jeff Moss,Joe Grand,Winn Schwartau,Limor Fried/ladyada,Bre Pettis,Kevin Mitnick,Emmanuel Goldstein',0,1,0,0),(9,'The Simpsons',NULL,NULL,',Bart,Lisa,Homer,Moe,Dr. Nick,Santas Little Helper,Troy McClure',0,1,0,0),(10,'Dr. Who',NULL,NULL,',TARDIS,Time Lords,Dalek,Sonic Screwdriver,Cybermen,K9,Weeping Angels',0,0,0,0),(11,'Virtuallity',NULL,NULL,',ESX,Xen,KVM,Virtual Box,Hyper-V,QEMU,Parallels',0,0,0,0),(12,'Historically Significant Computers',NULL,NULL,',Difference Engine,Eniac,PDP,Apple I,Commodore 64,TRS-80,UNIVAC',0,0,0,0),(13,'Three Letter Agencies 1','The Feds!',NULL,',DEA,CIA,FBI,NSA,ATF,FCC,TSA',0,1,0,0),(14,'Three Letter Agencies 2','Technology',NULL,',AMD,FSF,OSI,MIT,SGI,DOE,ESA',0,0,0,0),(15,'Airport Fun!',NULL,NULL,',TSA,Long lines,Delays,Bad Food,Secondary Screenings,Standby Seats,(Sniffer) Dogs',0,0,0,0),(16,'Four Letter Agencies','Warning: Includes Canadian Content',NULL,',NASA,NOAA,RIAA,MPAA,RCMP,CSIS,CRTC',0,0,0,0),(17,'Cats',NULL,NULL,',Schrödinger,Hobbes,Ceiling,LOL,Long,Garfield,Hobbes',0,0,0,0),(18,'Nikita-tastic','Not responsible for this one at all (except I am)','Nikita',',Kruschev,La Femme,Elton John,Neil (aka Nikita\'s bitch),Tottenkoph (aka Fake-Nikita),Kronenberg,Caine',0,0,0,0),(19,'Comic Strips','all in geek fun',NULL,',xkcd,Dilbert,userfriendly,pennyarcade,Ctrl Alt Del,Calvin and Hobbes,Least I Could Do',0,0,0,0),(20,'What\'s in a *NIX?','Linux Distributions',NULL,',Yellow Dog,Mint,Fedora,Gentoo,Slackware,Untangle,Mythbuntu',0,0,0,0),(21,'Fictional Doctors',NULL,NULL,',Nick,McCoy,Who,Frankenstein,Hubert J. Farnsworth,Baltar,Strangelove',0,0,0,0),(22,'Freedom Writers',NULL,NULL,',Lawrence Lessig,RMS,ESR,Pamela Jones,Michael Geist,Thomas Jefferson,Cory Doctorow',0,1,0,0),(23,'Papers Please!','ID Yourself Citizen!',NULL,',Drivers License,Passport,SSN/SIN,Green Card,Birth Certificate,Voter registration,REALID',0,0,0,0),(24,'I got 99 Problems','But a bitch ain\'t one!',NULL,',Flat Tire,Dead Hard Drive,GPS Failure,Bad credit,No wireless,Dead battery,Incompatible format',0,1,0,0),(25,'Con Con','Everywhere a Con',NULL,',Cleveland - OH,Las Vegas - NV,Toronto - ON, New York - NY,Vancouver - BC,Washington - DC,Berlin - Germany',0,0,0,0),(26,'Liquid Love','Caffeinated Beverages',NULL,',Coffee,RedBull,Mountain Dew,Club Mate,Tea,Bawls,Buzz Water',0,0,0,0),(27,'Saturday Morning Cartoons','In the \'80s',NULL,',Transformers,GI Joe,Thundercats,Silverhawk,Mask,Voltron,He-MAN',0,0,0,0),(28,'Certifiable',NULL,NULL,',CISSP,CEH,CCNA,MCSE,LPIC,A+,RHCE',0,0,0,0),(29,'Networking 1','Companies',NULL,',Linksys,Juniper,Cisco,D-Link,TP Link,SMC,3Com',0,0,0,0),(30,'Networking 2','Socially',NULL,',,Twitter,LinkedIn,myspace,Identi.ca,Four Square,Blippy,Facebook',0,0,0,0),(31,'Musik',NULL,NULL,',KMFDM,Nine Inch Nails,Dual Core,DJ Jackalope,YT Cracker,Futuristic Sex Robots,MC Frontalot',0,1,0,0),(32,'1337 Munchies','Preferred Hack Snacks',NULL,',Mountain Dew,Bawls,Pizza,Cheetos,Sushi,Top Ramen,Bacon',0,0,0,0),(33,'L0phty Heights','From the Heavy Industries','Space Rogue',',Whacked Mac,POCSAG decoder,l0phtcrack,congress,advisory,bbs,Black Crawling Systems',0,1,0,0),(34,'Failed DC contests','games gone wrong',NULL,',Pin the tail on Banshee,Spot the Priest,5 mins in the skybox,badge wearing contest,World\'s #1 Hacker,Be a Sheep,Hacker Pyramid',0,1,0,0),(35,'Electronic Components',NULL,'Joe Grand',',Nixie tube,LED,EEPROM,op-amp,battery,quartz crystal,relay',0,0,0,0),(36,'Security Podcasts','May not include podcasts about security','Chris Nickerson',',Exotic Liability,Security Justice,Security Now,Hak5,Paul Dot Com,SHITcast,network security podcast',0,1,0,0),(37,'International Super Hackers',NULL,'Chris Nickerson',',Greg Evans,Ligatt,Greg Evans,Ligatt,Greg Evans,Ligatt,Greg Evans',0,0,0,0),(38,'Superheroes',NULL,NULL,',Aqua Man,Thor,Green Lantern,Wonder Woman,Ironman,The Hulk,Batman',0,0,0,0),(39,'Superhero Sidekicks','Everyone needs a right hand man',NULL,',Alfred,Tonto,Robin,Kato,Lois Lane,Launchpad McQuack,War Machine',0,0,0,0),(41,'Meme! Meme! Meme!','Memes!',NULL,',YOLO,planking,I took an arrow in my knee,Shit $X Says,Rage Face,Trololo,Imma Let you finnish...',0,0,0,0),(42,'Star*',NULL,NULL,',Trek,Wars,System,Burst,Gate,Light,Office',0,0,0,0),(43,'*Star',NULL,NULL,',Battle,North,Death,Falling,Rock,Lone,Porn',0,0,0,0),(44,'Obsolete Data Storage Media',NULL,NULL,',zip disk,floppy disk,9-track tape,audio cassette tape,Punch Cards,Mini disc,Laser Disc',0,0,0,0),(45,'Hacker TV Shows',NULL,NULL,',Level 9,Lone Gunman,Tiger Team,Mythbusters,Ghost in the Shell,Net Force,Prototype This!',0,1,0,0),(46,'Micro',NULL,NULL,',Cassette,Soft,Film,Super,Scopic,USB,Machines',0,0,0,0),(47,'Hardware Hacking Reality Shows',NULL,NULL,',Junkyard Wars,Mythbusters,Prototype This,Smash Lab,Weaponizers,Make TV,History Hacking',0,0,0,0),(48,'Movie Hacker Characters',NULL,NULL,',Neo - The Matrix,Martin Bishop - Sneakers,R2D2 - Star Wars,Napster - Italian Job (2003),Stanley Jobson - Swordfish,Edward \"Brill\" Lyle - Enemy of the State,Crash Override - Hackers',0,0,0,0),(49,'Star Trek Hack or Crash',NULL,NULL,',Return of the Archons (Landru),The Changeling (Nomad),The Ultimate Computer (M-5),That Which Survives (Losira),I Mudd (Norman),ST2-WoK - Kobiayashi Maru,ST2009 - Kobayashi Maru',0,0,0,0),(50,'Mythbuster Rip Off Shows',NULL,NULL,',Smash Lab,Time Warp,Deadliest Warrior,Deestroy Build Destroy,Dude... What Would Happen?,Weapons Masters,Unsolved History',0,1,0,0),(51,'Malware Ports',NULL,NULL,',12345 (Netbus),3127 (My.Doom.A),3128 (My.Doom.B),5554 (Sasser),27374 (Subseven),17300 (Kuang2),2283 (Dumaru.Y)',0,0,0,0),(52,'Cyberpunk Novels',NULL,NULL,',Neuromancer,Count Zero,Mona Lisa Overdrive,Snow Crash,Diamond Age,Shockwave Rider,Islands in the Net',0,1,0,0),(53,'CPU types',NULL,NULL,',Pentium 4,Pentium Pro,AMD K6-2,Athlon,Celeron,Duron,Cyrix',0,0,0,0),(54,'Email Providers',NULL,NULL,',GMAIL,Yahoo,Hotmail,FastMail,Inbox.com,HotPOP,Mail.com',0,0,0,0),(55,'Mix it up!','Things you can mix with Jack Daniels',NULL,',ice cubes,Coke,Cheerios,Bawls,Shmoobus,Dan Kaminsky,sec b-sides',0,0,0,1),(56,'Pyramid Celebs',NULL,NULL,',Billy Crystal,William Shatner,Jason Alexander,Billy Crystal,Betty White,John Ritter,Penn Gillette',0,0,0,1),(58,'Electronic Components',NULL,NULL,',Resistor,Capacitor,Inductor,Transformer,conductor,diode,sensor',0,0,0,1),(59,'Password Fail','Commonly Used Passwords',NULL,',God,Password,QWERTY,cisco,admin,secret,r00t',0,0,0,1),(60,'Clear Text Protocol',NULL,NULL,',FTP,SMTP,TELNET,RSH,SNMP,HTTP,POP3',0,0,0,1),(61,'Microprocessor Love',NULL,NULL,',Z80,8086,Pentium,68000,6509,Atom,4004',0,1,0,1),(62,'Phreakin\' Me Out',NULL,NULL,',2600Hz,DTMF,\"Joybubbles\" or Joe Engressia,Phone Losers of America,LOD (Legion of Doom),Blue Box,Operation Sun Devil',0,0,0,1),(63,'Mystery Seven','Things you might find in a hacker\'s backpack',NULL,',USB Drive,Mouse,Sunglasses,Swiss Army Knife,Notebook,USB Adapter,A Dropbox/PwnPlug/minipwner',0,0,0,1),(64,'Name it.','Words that begin with Q',NULL,',Queue,Quaalude,Quiz,Quandry,Quarantine,Queen,Quark',0,0,0,1),(65,'What\'s on top?','Pizza toppings',NULL,',onions,banana peppers,blueberries,mozzarella cheese,pineapple,mozzarella cheese,pepperoni',0,0,0,1),(66,'What\'s in a name','Famous Hackers',NULL,',Zero Cool,Kevin Mitnick,Robert Morris Jr.,The Dark Tangent,Steve Wozniak,Alan Turing,MafiaBoy',0,0,0,1),(67,'Microsoftisms',NULL,NULL,',BSoD,Start Button,Clippy,Driverhell,Vista Home Basic,BSD code,Ctrl+Alt+Delete',0,0,0,1),(68,'Other Cons',NULL,NULL,',HAR,Notacon,RECon,ShmooCon,Hack-in-the-Box,ToorCon,SecTor',0,1,0,1),(69,'Hacker Kryptonite',NULL,NULL,',Business Suits,soap,9-to-5,meetings,rules,easy listening,smurfs,',0,0,0,1),(70,'Pyramid Celebs',NULL,NULL,',Billy Crystal,William Shatner,Jason Alexander,Billy Crystal,Betty White,John Ritter,Penn Gillette',0,0,0,1),(71,'Hackerspace $home',NULL,NULL,',Brussels,Chicago,Toronto,Kansas City,Helsinki,Walla Walla,Indianapolis',0,1,0,1),(72,'Indicted ',NULL,NULL,',Li\'l Hacker,Adrian Lamo,Kevin Mitnick,Phiber Optik,Kevin Poulsen,PirateBay,Gary McKinnon',0,1,0,1),(73,'Memories of the AP',NULL,NULL,',tent,goon pool,hot tub,pool three girl,Defcon TV,Liquor/Super Mart, haxxxor Girls',0,1,0,1),(74,'D. M. C. A.',NULL,NULL,',Dmitry Sklyarov,Fair Use,Take down,Apple,youtube,Title 17,Village People',0,1,0,1),(75,'Wireless Violations',NULL,NULL,',SSID Broadcast,Discoverable,Kismet,Blue Tooth,WEP,Infared,Keyboards',0,1,0,1),(76,'Found: 1 Dan K.','Places you can find a drunk Dan Kaminsky',NULL,',Defcon audience,Defcon Podium,Seattle,Pool Three,Shadow Bar,Twitter,Elevator',0,0,0,1),(77,'Mystery 7','impulse buys',NULL,',lottery tickets,Playboy,flashlights,Sharpies,potato chips,Crown Royal ,DVDs',0,1,0,1),(78,'AquaNet','80s hair bands',NULL,',Poison ,Van Halen,Ratt,Quiet Riot,Skid Row,Cinderella,Def Leppard',0,0,0,1),(79,'My Little Pwnie 07','People who won a pwnie award in 2007',NULL,',Halvar Flake,Dave Aitel,HD Moore,Symantec,Mark Dowd,Dave Maynor,OpenBSD team',0,1,0,1),(80,'Desk-cessories','Things you might find on a hacker\'s desktop',NULL,',Old Ram,Access Card,energy drink,coffee,rabbit\'s foot,fast food ,floppy disk',0,0,0,1),(81,'Turn Offs','Things you should disable at Defcon',NULL,',bluetooth,wireless,netbios ,autoplay,paypass,cookies,mDNSresponder',0,0,0,1),(82,'Sales','Things you do in a Sales meeting',NULL,',Twitch,Lie,Laugh ,Text Message,Sleep,Email,Ebay',0,0,0,1),(83,'Hacker Assumptions','Things your mom secretly thinks you can hack.',NULL,',Launch Codes,Email,TV,Oil Tankers,Voting,Credit Cards,Pentegon',0,0,0,1),(84,'Nick Farr','Things you can associate with Nick Farr',NULL,',Burgers,Sushi,Hacker spaces,Accounting,hackers on a plane,eating contests,speaker',0,0,0,1),(85,'Hardware Hacked','Voiding your warranty, hardware that has been hacked.',NULL,',wii-mote,roomba,netbooks,rfid,toliets,gps,road signs',0,0,0,1),(86,'Buzzword Bingo','Over used in recent media',NULL,',Cloud,PCI,Cyber-War,Web 2.0,Chrome OS,php,iphone',0,0,0,1),(87,'Skyboxes','Things that will get you into a skybox party',NULL,',Password,Secret Handshake,Breasts,Strippers,Alcohol,Goon badge,Social Engineering',0,1,0,1),(88,'Pwnd','Things that will destroy us all...',NULL,',Robots,Zombies,The Matrix,SkyNet,Asteroid,Aliens,y2k',0,0,0,1),(89,'Shoo Fly','Things that are irritating',NULL,',mosquito bites,stupid people,delayed flights,telemarketers,fingers on chalkboard,Conference Calls,Windows',0,0,0,1),(90,'Zie Germans',NULL,NULL,',Chaos Computer Club,Tron,Halvar Flake,Felix Lindner,\"Anti-Hacker\" Law ,Blinkenlights,Toralv Dirro',0,0,0,1),(91,'The Holy Grail','Monty Pythons Holy grail',NULL,',Flesh wound,air-speed velocity,Huge Tracts of Land,Lady of the Lake,A herring,Spam,Holy Hand Grenade',0,0,0,1),(92,'What Happens in Vegas','Things associated with LV',NULL,',prostitution,bachelor parties,the mafia,wedding chapels,gambling,neon lights,Donny and Marie',0,0,0,1),(93,'Mix it up!','Things you can mix with Jack Daniels',NULL,',ice cubes,Coke,Cheerios,Bawls,Shmoobus,Dan Kaminsky,sec b-sides',0,1,0,1),(94,'By the Numbers ^2','Name the Port Number based off description',NULL,',IRC ( 194) ,NTP (123),HTTP (80),SMTP (25) ,FTP (21),TELNET (23),SSH (22)',0,0,0,1),(95,'Harder than it looks','Things associated with game shows',NULL,',briefcases,Vanna White,pyramid,Whammys,Phone a Friend,Drew Carey,big hair',0,0,0,1);
/*!40000 ALTER TABLE `catagories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status` (
  `type` text NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status`
--

LOCK TABLES `status` WRITE;
/*!40000 ALTER TABLE `status` DISABLE KEYS */;
INSERT INTO `status` VALUES ('endpoint',0),('timer',1371607956);
/*!40000 ALTER TABLE `status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teams`
--

DROP TABLE IF EXISTS `teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teams` (
  `team_id` int(2) NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  `celeb` text NOT NULL,
  `participant` text NOT NULL,
  `score` int(11) NOT NULL,
  PRIMARY KEY (`team_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teams`
--

LOCK TABLES `teams` WRITE;
/*!40000 ALTER TABLE `teams` DISABLE KEYS */;
/*!40000 ALTER TABLE `teams` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-06-24 10:36:42
