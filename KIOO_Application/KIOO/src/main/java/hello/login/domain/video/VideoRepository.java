package hello.login.domain.video;


import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Repository
public class VideoRepository {
    private static final Map<Long, Video> store = new HashMap<>(); //static
    private static long sequence = 0L; //static

    public Video save(Video video) {
        video.setId(++sequence);
        store.put(video.getId(), video);
        return video;
    }

    public Video findById(Long id){
        return store.get(id);
    }

    public List<Video> findAll(){
        return new ArrayList<>(store.values());
    }

    public void update(Long videoId, Video updateParam){
        Video findVideo = findById(videoId);
        findVideo.setDate(updateParam.getDate());
    }


    public void clearStore() {
        store.clear();
    }
}
