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

  Items = []

  def __init__(self, url):
    file = urllib.urlopen(url)
    
    xml.sax.parse(file, self)

    self.Link = url.lower().strip()
    
  def startElement(self, RawName, attrs):
    Name = RawName.lower()
    if Name == "item":
      self.currentSubHandler = Item()
      self.Items.append(self.currentSubHandler)
    elif self.currentSubHandler != None:
      self.currentSubHandler.startElement(RawName, attrs)
    else:
      self.Content = ""

  def characters(self, RawContent):
    if self.currentSubHandler != None:
      self.currentSubHandler.characters(RawContent)
    else:
      self.Content += RawContent.strip()

  def endElement(self, RawName):
    Name = RawName.lower()
    if Name=="item":
      self.currentSubHandler = None
    elif self.currentSubHandler != None:
      self.currentSubHandler.endElement(RawName)
    elif Name == "title":
      self.Title = self.Content
    elif Name == "description":
      self.Description = self.Content
    elif Name == "pubdate":
      self.PubDate = rfc822toDateTime(self.Content)
    elif Name == "link":
      pass
      #self.Link = self.Content
    elif Name == "guid":
      self.GUID = self.Content

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

  def close(self):
    print(self.__dict__) 

def rfc822toDateTime(content):
  return datetime.datetime(*email.utils.parsedate(content)[:7])


