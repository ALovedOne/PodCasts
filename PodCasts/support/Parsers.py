import xml.sax
import urllib
import datetime
import email
import traceback

class RSSParser (xml.sax.handler.ContentHandler):
  currentSubHandler = None
  Content = ""
  
  Title = ""
  Description = ""
  PubDate = ""
  Link = ""
  GUID = ""
  MediaURL = ""
  MediaSize = ""
  MediaType = ""
  ImageLink = ""

  Items = None
  Elements = None

  def __init__(self, url):
    self.Items = []
    self.Elements = []
    self.Link = url.lower().strip()
    f = urllib.urlopen(self.Link)
    xml.sax.parse(f, self)
    f.close()

    
  def startElement(self, RawName, attrs):
    Name = RawName.lower()
    self.Elements.append(Name)
    if Name == "item":
      self.currentSubHandler = Item()
      self.Items.append(self.currentSubHandler)
      self.Content = ""
    elif self.currentSubHandler != None:
      self.currentSubHandler.startElement(RawName, attrs)
    elif Name == "itunes:image":
      if self.ImageLink == "":
        self.ImageLink = attrs.getValue("href")
    else:
      self.Content = ""

  def characters(self, RawContent):
    if self.currentSubHandler != None:
      self.currentSubHandler.characters(RawContent)
    else:
      self.Content += RawContent.strip()

  def endElement(self, RawName):
    Name = RawName.lower()
    self.Elements.pop()
    if Name=="item":
      self.currentSubHandler = None
    elif self.currentSubHandler != None:
      self.currentSubHandler.endElement(RawName)
    elif Name == "title":
      self.Title = self.Content
    elif Name == "description":
      self.Description = self.Content
    elif Name == "pubdate":
      try:
        self.PubDate = rfc822toDateTime(self.Content)
      except Exception as e:
        self.PubDate = datetime.now()
        print e
    elif Name == "link":
      pass
      #self.Link = self.Content
    elif Name == "guid":
      self.GUID = self.Content
    elif Name=="url" and self.Elements[-1]=="image":
      if self.ImageLink == "":
        self.ImageLink = self.Content

  def __repr__(self):
    return repr(self.__dict__)

class Item(xml.sax.handler.ContentHandler):
  Content = ""
  
  Title = ""
  Description = ""
  PubDate = ""
  Link = ""
  GUID = ""
  MediaURL = ""
  MediaSize = ""
  MediaType = ""

  def __init__(self):
    pass
    
  def startElement(self, RawName, attrs):
    Name = RawName.lower()
    self.Content = ""
    if Name == "enclosure":
      self.MediaURL = attrs.getValue("url")
      self.MediaSize = attrs.getValue("length")
      self.MediaType = attrs.getValue("type")
    else:
      self.LastTag = Name

  def characters(self, RawContent):
    self.Content += RawContent.strip()

  def endElement(self, RawName):
    Name = RawName.lower()
    if Name == "title":
      self.Title = self.Content
    elif Name == "description":
      self.Description = self.Content
    elif Name == "pubdate":
      self.PubDate = rfc822toDateTime(self.Content)
    elif Name == "link":
      self.Link = self.Content
    elif Name == "guid":
      self.GUID = self.Content

  def __repr__(self):
    return str(self.__dict__)

def rfc822toDateTime(content):
  dte = email.utils.parsedate(content)
  if dte == None:
    return datetime.datetime.now()
  return datetime.datetime(*email.utils.parsedate(content)[:7])


